#Import 
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


#Write Logic

class ProgressReport(Base):
    __tablename__ = "progress_reports"

    # id, userr_id, course_id, progress_percentage, status, feedback, remarks, created_at, updated_at
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    progress_percentage = Column(Float, default=0.0, nullable=False)
    status = Column(String(50), nullable=False, default="not_started")
    feedback = Column(Text, nullable=True)
    remarks = Column(String(80), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
