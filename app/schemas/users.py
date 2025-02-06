from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.users import UserRole


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    role: UserRole

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    role: Optional[UserRole]
