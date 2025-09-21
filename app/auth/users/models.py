from sqlalchemy import Column, Text, Integer, Boolean, String
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(50), nullable=False)
    email = Column(String(40), nullable=False, unique=True)
    phone_number = Column(String(15), nullable=True) 
    password = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)