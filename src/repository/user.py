from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.core.security import Security
from src.model.user import User_Class
from src.model.enum import UserRole
from src.utils.loggers import get_logger

logger = get_logger(__name__)


class UserRepository:

    @staticmethod
    def create(payload: User_Class, db: Session) -> User_Class:
        if isinstance(payload, User_Class):
            new_user = payload
            if new_user.user_role is None:
                new_user.user_role = UserRole.USER
        else:
            role = payload.user_role if hasattr(payload, "user_role") and payload.user_role is not None else UserRole.USER
            new_user = User_Class(
                user_name = payload.user_name,
                user_email = payload.user_email,
                user_password = payload.user_password,
                user_contact = payload.user_contact,
                user_role = role,
                user_pincode = payload.user_pincode,
                user_department_id = payload.user_department_id
            )
        logger.info(f"Creating user with payload: {payload}")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"User created successfully: {new_user}")
        return new_user

    @staticmethod
    def get_by_id(user_id: int, db: Session) -> User_Class | None:
        return db.query(User_Class).filter(User_Class.user_id == user_id).first()

    @staticmethod
    def get_by_email(user_email: str, db: Session) -> User_Class | None:
        return db.query(User_Class).filter(User_Class.user_email == user_email).first()

    @staticmethod
    def list_all(db: Session) -> list[User_Class]:
        return db.query(User_Class).all()

    @staticmethod
    def delete(payload: User_Class, db: Session) -> None:
        db.delete(payload)
        db.commit()
