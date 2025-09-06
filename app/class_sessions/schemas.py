from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Base schema - common fields
class ClassSessionBase(BaseModel):
    course_id: int = Field(..., description="ID of the course")
    instructor_id: int = Field(..., description="ID of the instructor user")
    date_time: datetime = Field(..., description="Start date and time of the class")
    duration: float = Field(..., description="Duration in hour")
    is_active: bool = Field(True, description="Whether the class session is active")

# Create schema - for creating new class sessions
class ClassSessionCreate(ClassSessionBase):
    pass

# Update schema - for updating existing class sessions
class ClassSessionUpdate(BaseModel):
    date_time: Optional[datetime] = Field(None, description="Start date and time of the class")
    duration: Optional[int] = Field(None, description="Duration in hours")
    is_active: Optional[bool] = Field(None, description="Whether the class session is active")

# Response schema - what gets returned from API
class ClassSessionInDBBase(ClassSessionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Enable ORM mode

class ClassSession(ClassSessionInDBBase):
    pass

# Optional: for internal database operations
class ClassSessionInDB(ClassSessionInDBBase):
    pass