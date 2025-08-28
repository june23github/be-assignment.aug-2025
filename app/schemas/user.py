from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models import UserRole
from schemas import BaseSchema

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.MEMBER

class UserCreate(UserBase):
    password: str
    organization_id: int

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase, BaseSchema):
    id: int
    is_active: bool
    organization_id: int
    created_at: datetime
    updated_at: Optional[datetime]

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None