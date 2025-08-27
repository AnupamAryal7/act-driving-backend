# import part
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import re


class UserBase(BaseModel):
    email: str = Field(..., description="user email address")
    role: str = Field(..., description="role field for student, instructor and admin")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password must contain atleast 6 character")

    @field_validator('role')
    @classmethod
    def validate_role(cls,v:str) -> str:
        valid_roles = ["student", "instructor", "admin"]
        if v not in valid_roles:
            raise ValueError(f'Roles must be one of {", ".join(valid_roles)}')
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v:str)->str:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Incorrect Email address')
        return v
    


class UserResponse(UserBase):
    id:int = Field(..., description="User id")

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email:str = Field(..., description="Email id required")
    password:str = Field(..., description="password field")