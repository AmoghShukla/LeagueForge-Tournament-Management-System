from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.dependencies.auth import required_role
from src.database.session import get_db
from src.schema.user import UserResponse, UserCreate, UserUpdate
from src.service.user import UserService

router = APIRouter(prefix="/user", tags=['User'])


@router.post('/', response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(payload, db)


@router.get('/{user_id}', response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.get_user(user_id, db)


@router.get('/', response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db), user = Depends(required_role(['ADMIN']))):
    return UserService.list_users(db)


@router.put('/{user_id}', response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    return UserService.update_user(user_id, payload, db)


@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db),  user = Depends(required_role(['ADMIN']))):
    return UserService.delete_user(user_id, db)