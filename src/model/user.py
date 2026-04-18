from src.database.base import Base
from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from src.model.enum import UserRole

class User_Class(Base):
    __tablename__="User"

    user_id = Column(Integer, primary_key=True, nullable=False)
    user_name = Column(String, nullable=False)
    user_email = Column(String, nullable=False, unique=True, index=True)
    user_password = Column(String, nullable=False)
    user_contact_no = Column(String)
    user_role =  Column(SQLAlchemyEnum(UserRole), default=UserRole.USER)
