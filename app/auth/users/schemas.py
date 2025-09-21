from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import re

class UserBase(BaseModel):
    full_name: str = Field(..., description="Full name of the user")
    email: str = Field(..., description="User email address")
    phone_number: Optional[str] = Field(None, description="User phone number (optional)")
    role: str = Field(..., description="Role field for student, instructor and admin")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password must contain at least 6 characters")

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        valid_roles = ["student", "instructor", "admin"]
        if v not in valid_roles:
            raise ValueError(f'Roles must be one of {", ".join(valid_roles)}')
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Incorrect Email address')
        return v

class UserResponse(UserBase):
    id: int = Field(..., description="User id")

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str = Field(..., description="Email id required")
    password: str = Field(..., description="password field")

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, description="Full name of the user")
    phone_number: Optional[str] = Field(None, description="User phone number (optional)")
    role: Optional[str] = Field(None, description="Role field for student, instructor and admin")
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            valid_roles = ["student", "instructor", "admin"]
            if v not in valid_roles:
                raise ValueError(f'Roles must be one of {", ".join(valid_roles)}')
        return v