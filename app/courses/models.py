from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, Double
from sqlalchemy.sql import func
from app.database import Base

class Course(Base):
    __tablename__ = "courses"

    # id, title, description, bullet_p123. duraction, packagetupe, total proce, disco proice, is active. created at, updated at

    id = Column(Integer, primary_key=True, index=True)
    course_title = Column(String(50), nullable= False)
    description = Column(Text, nullable=False)
    bullet_pt1 = Column(String(80), nullable=False)
    bullet_pt2 = Column(String(80), nullable=False)
    bullet_pt3 = Column(String(80), nullable=False)
    duration = Column(String(25), nullable=False)
    package_type = Column(String(20), nullable=False)
    total_price = Column(Double, nullable= False)
    discounted_price = Column(Double, nullable=True)
    is_active = Column(Boolean, default=True)
    image_url = Column(String(500), nullable=True)
    image_public_id = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
