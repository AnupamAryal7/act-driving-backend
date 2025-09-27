from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Base schema - common fields
class BookingBase(BaseModel):
    student_id: int = Field(..., description="ID of the student user")
    class_id: int = Field(..., description="ID of the class session")
    phone_no: str = Field(..., description="phone number of student")
    subrub: str = Field(None, description="pickup subrub of the students")
    additional_message: str
    status: str = Field("pending", description="Booking status: pending, confirmed, cancelled, attended, no_show")
    remarks: Optional[str] = Field(None, description="Additional remarks or notes")

# Create schema - for creating new bookings
class BookingCreate(BookingBase):
    pass

# Update schema - for updating existing bookings
class BookingUpdate(BaseModel):
    phone_no: Optional[str] = Field(None, description="update phone number")
    subrub: Optional[str] = Field(None, description="Update student pickup loacation")
    status: Optional[str] = Field(None, description="Booking status: pending, confirmed, cancelled, attended, no_show")
    remarks: Optional[str] = Field(None, description="Additional remarks or notes")
    additional_message: Optional[str]

# Response schema - what gets returned from API
class BookingInDBBase(BookingBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Booking(BookingInDBBase):
    pass

class BookingInDB(BookingInDBBase):
    pass