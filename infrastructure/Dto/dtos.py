from pydantic import BaseModel, Field
from datetime import datetime

class UserRegister(BaseModel):
    username : str = Field(...)   
    email : str = Field(..., description="Email should be valid")
    hashed_password  : str = Field(..., description="Enter valid Password")
    
    
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
        
        