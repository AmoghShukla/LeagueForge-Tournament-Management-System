from datetime import datetime, timedelta
from src.core.config import settings
from passlib.context import CryptContext
import jwt

password_context = CryptContext(schemes=['bcrypt_sha256', 'bcrypt'], deprecated='auto')

class Security:

    @staticmethod
    def hash_password(plain_password : str):
        if not isinstance(plain_password, str):
            raise ValueError("Password must be a string")
        if len(plain_password.encode('utf-8')) > 72:
            raise ValueError("Password too long (max 72 bytes)")
        return password_context.hash(plain_password)
    
    # @staticmethod
    # def verify_password(plain_Password, hash_password):
    #     return password_context.verify(plain_Password, hash_password)
    
    @staticmethod
    def create_access_token(data : dict):
        data_to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        data_to_encode.update({'exp' : expire})
        return jwt.encode(data_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    @staticmethod
    def create_refresh_token(data : dict):
        data_to_encode = data.copy()
        expire = datetime.now() + timedelta(hours=settings.REFRESH_TOKEN_EXPIRE_HOURS)

        data_to_encode.update({'exp' : expire})
        return jwt.encode(data_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)