from sqlalchemy.orm import Session
from infrastructure.Dto.dtos import UserDetails, UserLogin, UserRegister
from domain.models import User
from datetime import datetime
from fastapi import HTTPException
from .auth_functions import verify_password, get_password_hash, create_access_token, decode_access_token

class AuthService():
    def __init__(self, db : Session):
        self.db = db
    
    
    def register(self, user: UserRegister) -> UserDetails:
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

        self.db.add(newUser)
        self.db.commit()
        self.db.refresh(newUser)        
        return newUser 
    
        
    def getUsers(self) -> list[UserDetails]:
        return self.db.query(User).all()
    
        
    def login(self, user : UserLogin):
        u = self.db.query(User).filter( User.email == user.email ).first()
        if u is None:
            raise HTTPException(
                status_code=404,
                detail = "No user registered"
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
        
    