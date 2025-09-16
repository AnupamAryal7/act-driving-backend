from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CourseBase(BaseModel):
    course_title: str = Field(..., max_length=50, description="length must be less than 50 characters")
    description: str
    bullet_pt1: str = Field(..., max_length=80)
    bullet_pt2: str = Field(..., max_length=80)
    bullet_pt3: str = Field(..., max_length=80)
    duration: str = Field(..., max_length=25)
    package_type: str = Field(..., max_length=20)
    total_price: float
    discounted_price: Optional[float] = None
    is_active: bool = True
    image_url: Optional[str] = None
    image_public_id: Optional[str] = None


class CourseCreate(BaseModel):
    """Schema for creating a course - excludes image fields as they're handled separately"""
    course_title: str = Field(..., max_length=50, description="length must be less than 50 characters")
    description: str
    bullet_pt1: str = Field(..., max_length=80)
    bullet_pt2: str = Field(..., max_length=80)
    bullet_pt3: str = Field(..., max_length=80)
    duration: str = Field(..., max_length=25)
    package_type: str = Field(..., max_length=20)
    total_price: float
    discounted_price: Optional[float] = None
    is_active: bool = True

class CourseUpdate(BaseModel):
    course_title: Optional[str] = None
    description: Optional[str] = None
    bullet_pt1: Optional[str] = None
    bullet_pt2: Optional[str] = None
    bullet_pt3: Optional[str] = None
    duration: Optional[str] = None
    package_type: Optional[str] = None
    total_price: Optional[float] = None
    discounted_price: Optional[float] = None
    is_active: Optional[bool] = None

class CourseInDBBase(CourseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Course(CourseInDBBase):
    pass

class CourseInDB(CourseInDBBase):
    pass

# Additional schema for image upload response
class ImageUploadResponse(BaseModel):
    url: str
    public_id: str