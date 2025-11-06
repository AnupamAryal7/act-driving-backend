from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    user_id: int
    user_name: str
    email: EmailStr
    rating: int
    comment: Optional[str] = None
    course_title: Optional[str] = None
    is_approved: bool = False

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    user_name: Optional[str] = None
    rating: Optional[int] = None
    comment: Optional[str] = None
    course_title: Optional[str] = None
    is_approved: Optional[bool] = None

class ReviewResponse(ReviewBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True