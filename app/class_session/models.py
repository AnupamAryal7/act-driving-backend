from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base



class ClassSession(Base):
    __tablename__ = "class_session"
    # id, course id, insturfctor_id , date time, duration, is active, created at, updated at
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    instructor_id = Column(Integer, ForeignKey("users.id(roles = instructor)"), nullable=False)