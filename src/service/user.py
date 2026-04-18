from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.core.security import Security
from src.model.user import User_Class
from src.repository.user import UserRepository

class UserService:

    @staticmethod
    def create_user(payload, db: Session):
        existing = UserRepository.get_by_email(payload.user_email, db)
        if existing:
            raise HTTPException(status_code=400, detail='User already exists')

        try:
            hashed_password = Security.hash_password(payload.user_password)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        user = User_Class(
            user_name=payload.user_name,
            user_email=payload.user_email,
            user_password=hashed_password,
            user_contact_no=payload.user_contact_no
        )
        return UserRepository.create(user, db)

    @staticmethod
    def get_user(user_id: int, db: Session):
        user = UserRepository.get_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        return user

    @staticmethod
    def list_users(db: Session):
        return UserRepository.list_all(db)

    @staticmethod
    def update_user(user_id: int, payload, db: Session):
        user = UserRepository.get_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')

        if payload.user_email and payload.user_email != user.user_email:
            duplicate = UserRepository.get_by_email(payload.user_email, db)
            if duplicate:
                raise HTTPException(status_code=400, detail='Email already in use')
            user.user_email = payload.user_email

        if payload.user_name is not None:
            user.user_name = payload.user_name
        if payload.user_contact_no is not None:
            user.user_contact_no = payload.user_contact_no
        if payload.user_password:
            try:
                user.user_password = Security.hash_password(payload.user_password)
            except ValueError as exc:
                raise HTTPException(status_code=400, detail=str(exc)) from exc

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(user_id: int, db: Session):
        user = UserRepository.get_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        UserRepository.delete(user, db)
        return {'message': 'User deleted successfully'}