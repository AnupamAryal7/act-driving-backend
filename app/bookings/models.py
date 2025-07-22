from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    course_title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    discount_price = Column(Float, nullable=True)
    original_price = Column(Float, nullable=False)
    lession_description_1 = Column(Text, nullable=True)
    lession_description_2 = Column(Text, nullable=True)
    lession_description_3 = Column(Text, nullable=True)
    user_name = Column(String(100), nullable=False)
    user_email = Column(String(255), nullable=False)
    booking_status = Column(String(45), default="pending")  # pending, confirmed, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())