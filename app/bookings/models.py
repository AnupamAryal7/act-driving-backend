from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.sql import func
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("class_sessions.id"), nullable=False)
    phone_no = Column(String(30), nullable=False)
    suburb = Column(String(100), nullable=True)
    additional_message = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="pending") 
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())