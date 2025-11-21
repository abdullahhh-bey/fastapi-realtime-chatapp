from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from infrastructure.database import get_db
from infrastructure.Dto.dtos import UserDetails, UserLogin, UserRegister
from application.auth_services import AuthService

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