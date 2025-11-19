from fastapi import FastAPI, Depends, HTTPException
from infrastructure.database import Base, engine
from infrastructure.database import get_db
from sqlalchemy.orm import Session
from domain.models import User
from presentation.authRouter import AuthRouter
 
app = FastAPI(
    title="ChatApp"
)
 
app.include_router(AuthRouter)
