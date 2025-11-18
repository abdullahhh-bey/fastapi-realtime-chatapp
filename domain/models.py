from infrastructure.database import Base, engine
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, nullable=False)
    username = Column(String , nullable=False, index=True)    
    email = Column(String, nullable=False)
    hashed_password = Column(String)
    isRegistered = Column(Boolean , default = False)
    createdAt = Column(DateTime , default = datetime.utcnow)


Base.metadata.create_all(bind=engine)
