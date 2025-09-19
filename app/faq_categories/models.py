from sqlalchemy import String, Integer, Column, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Faq_Category(Base):
    __tablename__ = "faq_categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())