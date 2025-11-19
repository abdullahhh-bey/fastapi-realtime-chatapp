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

