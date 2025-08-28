from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CourseBase(BaseModel):
    course_title: str
    description: str
    bullet_pt1: str
    bullet_pt2: str
    bullet_pt3: str
    duration: str
    package_type:str
    total_price: float
    discounted_price: Optional[float] = None
    is_active: bool = True



class CourseCreate(CourseBase):
    pass

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