from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CourseCreate(BaseModel):
    name: str
    code: str

class CourseResponse(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        from_attributes = True