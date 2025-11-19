from pydantic import BaseModel, Field
from datetime import datetime

class UserRegister(BaseModel):
    username : str = Field(...)   
    email : str = Field(..., description="Email should be valid")
    password  : str 
    
    
class UserLogin(BaseModel):
    email : str = Field(...)
    password : str = Field(...)
    
    
class UserDetails(BaseModel):
    id : int
    username : str   
    email : str
    isRegistered : bool
    createdAt : datetime
    
    class Config:
        from_attributes = True
        
        