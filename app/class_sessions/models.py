from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey, DateTime
from sqlalchemy.sql import func, text
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import timedelta
from app.database import Base



class ClassSession(Base):
    __tablename__ = "class_sessions"
    
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_time = Column(DateTime(timezone=True), nullable=False)
    duration = Column(Integer, nullable=False) 
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Hybrid property for end time calculation
    @hybrid_property
    def end_time(self):
        # Python-side calculation
        return self.date_time + timedelta(hours=self.duration)
    
    @end_time.expression
    def end_time(cls):
        # SQL-side calculation (uses PostgreSQL interval)
        return cls.date_time + text("interval '1 hour' * duration")