from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class BookingBase(BaseModel):
    course_title: str
    description: str
    discount_price: Optional[float] = None
    original_price: float
    lession_description_1: Optional[str] = None
    lession_description_2: Optional[str] = None
    lession_description_3: Optional[str] = None
    user_name: str
    user_email: EmailStr
    booking_status: str = "pending"

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    course_title: Optional[str] = None
    description: Optional[str] = None
    discount_price: Optional[float] = None
    original_price: Optional[float] = None
    lession_description_1: Optional[str] = None
    lession_description_2: Optional[str] = None
    lession_description_3: Optional[str] = None
    booking_status: Optional[str] = None

class BookingResponse(BookingBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True