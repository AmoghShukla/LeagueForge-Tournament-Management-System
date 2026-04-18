from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schema.auth import LoginResponse
from src.schema.user import UserResponse, UserCreate
from src.database.session import get_db
from src.service.auth import AuthService
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=['Auth'])


@router.post('/signup', response_model=UserResponse)
def signup(payload : UserCreate, db : Session = Depends(get_db)):
    return AuthService.signup(payload, db)
    
    

@router.post('/login', response_model=LoginResponse)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db : Session = Depends(get_db)):
    try:
        return AuthService.login(form_data, db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)