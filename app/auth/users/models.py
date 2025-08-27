from sqlalchemy import Column, Text, Integer, Boolean, String
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(40), nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False) # "student" "instructor" "admin"