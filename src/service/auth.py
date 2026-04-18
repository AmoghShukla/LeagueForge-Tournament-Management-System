from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.core.security import Security
from src.repository.user import UserRepository
from src.repository.auth import AuthRepository
from src.model.user import User_Class
from src.model.enum import UserRole


class AuthService:

    @staticmethod
    def signup(payload, db: Session):
        user = UserRepository.get_by_email(payload.user_email, db)

        if user:
            raise HTTPException(status_code=400, detail="User already exists, please login")

        
        role = UserRole.ADMIN if not AuthRepository.has_admin(db) else UserRole.USER

        new_user = User_Class(
            user_name=payload.user_name,
            user_email=payload.user_email,
            user_password=payload.user_password,
            user_contact_no=payload.user_contact_no,
            user_role=role
        )

        return UserRepository.create(new_user, db)

    @staticmethod
    def login(payload, db: Session):
        user = UserRepository.get_by_email(payload.username, db)

        if not user:
            raise HTTPException(status_code=404, detail="User does not exist, please signup")

        # if not Security.verify_password(payload.password, user.user_password):
        if not payload.password==user.user_password:
            raise HTTPException(status_code=401, detail="Invalid password")

        role_value = user.user_role.value if hasattr(user.user_role, 'value') else str(user.user_role)

        access_token = Security.create_access_token({
            'sub': str(user.user_id),
            'user_role': role_value,
            'token_type': 'access_token'
        })

        refresh_token = Security.create_refresh_token({
            'sub': str(user.user_id),
            'user_role': role_value,
            'token_type': 'refresh_token'
        })

        return {
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer'
        }