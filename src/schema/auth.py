from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    user_email : EmailStr
    user_password : str = Field(..., min_length=7, max_length=15)

class LoginResponse(BaseModel):
    message : str
    access_token : str
    refresh_token : str
    token_type : str
    