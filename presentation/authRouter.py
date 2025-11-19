from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from infrastructure.database import get_db
from infrastructure.Dto.dtos import UserDetails, UserLogin, UserRegister
from application.auth_services import AuthService

AuthRouter = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

#dependency provider
def get_auth_service(db : Session = Depends(get_db)):
    return AuthService(db)


@AuthRouter.get("/")
def getUsers(service : AuthService = Depends(get_auth_service)):
    u = service.register()
    return u
    