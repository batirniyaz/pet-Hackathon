from pydantic import BaseModel, EmailStr, constr
from typing import Optional, Union


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: constr(min_length=8, max_length=15)
    confirm_password: str

    @staticmethod
    def passwords_match(password: str, confirm_password: str) -> str:
        if password != confirm_password:
            raise ValueError('Passwords do not match')
        return confirm_password

    @staticmethod
    def password_complexity(password: str) -> str:
        import re
        if not re.findall(r'\d', password):
            raise ValueError('Password must contain at least one number')
        if not re.findall(r'[A-Z]', password) or not re.findall(r'[a-z]', password):
            raise ValueError('Password must contain both uppercase and lowercase letters')
        if not re.findall(r'\W', password):
            raise ValueError('Password must contain at least one special character')
        return password


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
