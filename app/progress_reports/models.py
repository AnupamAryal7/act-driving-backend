# todo 
#Import 
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


#Write Logic

class ProgressReport(Base):
    __tablename__ = "progress_reports"

    #id,student_id, instructor_id, course_id, status, feedback, created_at, updated_at
    id = Column(Integer, primary_key=True, index= True)
    student_id = Column(Integer, ForeignKey(sutdents.id),nullable=False )
    instructor_id = Column(Integer, ForeignKey(istructors.id), nullable=False)
    course_id = Column(Integer, ForeignKey(courses.id),nullable=False )
    status = Column(String(30), nullable=True)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
