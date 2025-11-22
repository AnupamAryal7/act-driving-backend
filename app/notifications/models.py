"""
Database models for push notifications
Stores FCM tokens and notification logs
"""
from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import uuid

# Use your existing Base import from database.py
from app.database import Base

def generate_uuid():
    """Generate UUID for primary keys"""
    return str(uuid.uuid4())


class UserFCMToken(Base):
    """
    Stores FCM tokens for each user device
    A user can have multiple tokens (multiple devices/browsers)
    """
    __tablename__ = "user_fcm_tokens"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False, index=True)
    user_type = Column(String, nullable=False)  # 'instructor' or 'student'
    fcm_token = Column(String, unique=True, nullable=False)
    device_info = Column(Text)  # Browser, device type info
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<UserFCMToken(user_id={self.user_id}, user_type={self.user_type})>"


class NotificationLog(Base):
    """
    Logs all notification attempts for auditing and debugging
    Helps track delivery success/failure
    """
    __tablename__ = "notification_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False, index=True)
    user_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    data = Column(JSON)  # Store additional data as JSON
    fcm_token = Column(String)
    success = Column(Boolean, default=False)
    error_message = Column(Text)
    sent_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<NotificationLog(user_id={self.user_id}, success={self.success})>"