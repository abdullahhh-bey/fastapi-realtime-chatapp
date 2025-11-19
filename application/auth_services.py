from sqlalchemy.orm import Session
from infrastructure.Dto.dtos import UserDetails, UserLogin, UserRegister
from domain.models import User

class AuthService():
    def __init__(self, db : Session):
        self.db = db
    
    def register(self):
        u = self.db.query(User).all()
        print("yes")
        return u
        
    def login():
        pass
        
    