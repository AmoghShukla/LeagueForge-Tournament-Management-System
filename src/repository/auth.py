from sqlalchemy.orm import Session

from src.model.user import User_Class
from src.model.enum import UserRole


class AuthRepository:

    @staticmethod
    def has_admin(db: Session) -> bool:
        return db.query(User_Class).filter(User_Class.user_role == UserRole.ADMIN).first() is not None
    