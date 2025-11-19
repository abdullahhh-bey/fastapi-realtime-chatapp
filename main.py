from fastapi import FastAPI, Depends, HTTPException
from infrastructure.database import Base, engine
from infrastructure.database import get_db
from sqlalchemy.orm import Session
from domain.models import User
 
app = FastAPI(
    title="ChatApp"
)
 
@app.get("/")
async def getUsers(db : Session = Depends(get_db)):
    users = db.query(User).all()
    if len(users) == 0:
        raise HTTPException(
            status_code=404,
            detail="No users yet! Soon"
        )
        
