from sqlalchemy.orm import Session
from infrastructure.Dto.dtos import UserDetails, UserLogin, UserRegister
from domain.models import User
from datetime import datetime
from fastapi import HTTPException
from .auth_functions import verify_password, get_password_hash, create_access_token, decode_access_token
from .email_service import send_email

class AuthService():
    def __init__(self, db : Session):
        self.db = db
    
    
    async def register(self, user: UserRegister) -> str:
        check = self.db.query(User).filter(User.email == user.email).first()
        if check:
            raise HTTPException(status_code=400, detail="Email already registered!")

        checkname = self.db.query(User).filter(User.username == user.username).first()
        if checkname:
            raise HTTPException(status_code=400, detail="Username already exists!")

        hashedPassword = get_password_hash(user.password)
        newUser = User(
            username=user.username,
            email=user.email,
            hashed_password=hashedPassword,
            isRegistered=False,
            createdAt=datetime.utcnow()  
        )   
        
        data = {
            "sub" : newUser.username,
            "email" : newUser.email
        }
        
        token = create_access_token(data)

        verification_link = f"Token: \n{token}\n"

        html = f"""
        <h3>Verify your account</h3>
        <p>Click below to verify:</p>
        <p>"Token: \n{token}\n"</p>
        """

        await send_email(newUser.email, "Verify Your Account", html)
                 
        self.db.add(newUser)
        self.db.commit()
        self.db.refresh(newUser)    
        return f'Hey {newUser.username},Verify your email for complete registration' 
    
    

    
    def verify_email(self, token : str) -> str:
        username = decode_access_token(token)
        userCheck = self.db.query(User).filter(User.username == username).first()
        if not userCheck:
            raise HTTPException(
                status_code=400,
                detail="Wrong Token"
            )
        
        userCheck.isRegistered = True
        self.db.commit()
        return "User successfully registered!"
        
        
    
    def getUsers(self) -> list[UserDetails]:
        return self.db.query(User).all()
    
        
    def login(self, user : UserLogin):
        u = self.db.query(User).filter( User.email == user.email ).first()
        if u is None:
            raise HTTPException(
                status_code=404,
                detail = "No user registered"
            )
            
        if not u.isRegistered:
            raise HTTPException(
                status_code=400,
                detail="User not registered the email, First complete the registration process!"
            ) 
            
        passwordCheck = verify_password(user.password , u.hashed_password)
        if not passwordCheck:
            raise HTTPException(
                status_code=400,
                detail="Wrong Password"
            )
        
        data = {
            "sub" : u.username,
            "email" : u.email, 
        }
        accessToken = create_access_token(data)
        return {
            "access-token" : accessToken
        } 
        
    
    