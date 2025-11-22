from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from infrastructure.Dto.dtos import UserDetails, UserLogin, UserRegister
from application.auth_services import AuthService
from application.websocket_manager import manager
from domain.models import Message, User
import json
from infrastructure.Dto.dtos import MessageCreate, MessageResponse
from typing import List


AuthRouter = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

#dependency provider
def get_auth_service(db : Session = Depends(get_db)):
    return AuthService(db)


@AuthRouter.post("/register")
async def register(user : UserRegister, service : AuthService = Depends(get_auth_service)):
    u = await service.register(user)
    return u

@AuthRouter.get("/users", response_model=list[UserDetails])
def getUsers(service : AuthService = Depends(get_auth_service)):
    u = service.getUsers()
    return u
    
@AuthRouter.post("/login")
def login(user : UserLogin, service : AuthService = Depends(get_auth_service)) -> dict:
    u = service.login(user)
    return u

@AuthRouter.post("/verify")
def verifyEmail(token : str, service : AuthService = Depends(get_auth_service)) -> str:
    s = service.verify_email(token)
    return s


@AuthRouter.post("/forgot/{token}")
async def forgotPassword(email : str , service : AuthService = Depends(get_auth_service)) -> str:
    s = await service.forgotPassword(email)
    return s

@AuthRouter.post("/reset/{token}")
def resetPassword(password : str , token : str, service : AuthService = Depends(get_auth_service)) -> str:
    s = service.resetPassword(password , token)
    return s

@AuthRouter.post("/change/password")
def changePassword(oldpass : str, newpass : str , email : str, service : AuthService = Depends(get_auth_service)) -> str:
    s = service.changePassword(email  ,oldpass , newpass)
    return s


@AuthRouter.websocket("/ws/chat/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
    db: Session = Depends(get_db)
):
    userCheck = db.query(User).filter( User.id == user_id ).first()
    if not userCheck:
        raise HTTPException(
            status_code=404,
            detail="User not registered!"
        )
    
    
    await manager.connect(websocket, user_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            db_message = Message(
                sender_id=user_id,
                receiver_id=message_data["receiver_id"],
                content=message_data["content"]
            )
            db.add(db_message)
            db.commit()
            db.refresh(db_message)
            

            message_response = {
                "id": db_message.id,
                "sender_id": db_message.sender_id,
                "receiver_id": db_message.receiver_id,
                "content": db_message.content,
                "created_at": db_message.created_at.isoformat()
            }
            
            await manager.send_personal_message(
                message_response, 
                message_data["receiver_id"]
            )
            

            await manager.send_personal_message(
                message_response,
                user_id
            )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        

@APIRouter.get("/chat/history/{user_id}/{other_user_id}", response_model=List[MessageResponse])
def get_chat_history(
    user_id: int,
    other_user_id: int,
    db: Session = Depends(get_db),
    limit: int = 50
):
    """
    Fetch chat history between two users
    """
    messages = db.query(Message).filter( Message.sender_id == user_id, Message.receiver_id == other_user_id).all()
    return messages