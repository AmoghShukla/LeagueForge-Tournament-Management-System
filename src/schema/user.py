from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    user_name : str = Field(...)
    user_email : EmailStr
    user_password : str = Field(..., min_length=1, max_length=12)
    user_contact_no : str = Field(..., min_length=10, max_length=10)

class UserResponse(BaseModel):
    user_id: int
    user_name : Optional[str]
    user_email : EmailStr
    user_contact_no : Optional[str]

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    user_email: Optional[EmailStr] = None
    user_password: Optional[str] = Field(default=None, min_length=8, max_length=72)
    user_contact_no: Optional[str] = Field(default=None, min_length=10, max_length=10)
