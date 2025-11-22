from infrastructure.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, nullable=False, primary_key=True)
    username = Column(String(150) , nullable=False, index=True)    
    email = Column(String, nullable=False)
    hashed_password = Column(String)
    isRegistered = Column(Boolean , default = False)
    createdAt = Column(DateTime , default = datetime.utcnow)

    

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))  
    receiver_id = Column(Integer, ForeignKey("users.id")) 
    content = Column(String, nullable=False)  
    created_at = Column(DateTime, server_default=func.now()) 

