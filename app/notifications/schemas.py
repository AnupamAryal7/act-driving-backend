"""
Pydantic schemas for push notifications
Used for request/response validation in API endpoints
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class FCMTokenRegister(BaseModel):
    """
    Schema for registering a new FCM token from frontend
    """
    user_id: str
    user_type: str  # 'instructor' or 'student'
    fcm_token: str
    device_info: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user_123",
                "user_type": "student", 
                "fcm_token": "fcm_token_abc123",
                "device_info": "Chrome on Windows"
            }
        }


class FCMTokenResponse(BaseModel):
    """
    Response after successfully registering FCM token
    """
    message: str
    token_id: str


class BookingNotificationData(BaseModel):
    """
    Data for booking notifications to instructors
    Contains minimal info needed for the notification
    """
    booking_id: str
    student_name: str  # We'll get this from student_id when creating booking
    booking_time: Optional[str] = None  # Optional: if you want to show time

class ProgressNotificationData(BaseModel):
    """
    Data for progress report notifications to students  
    Contains minimal info needed for the notification
    """
    progress_id: str
    # We don't need student_name since it's going TO the student
    # Just progress_id to link to the report


class NotificationRequest(BaseModel):
    """
    Schema for sending a notification to specific user
    """
    user_id: str
    title: str
    body: str
    data: Optional[Dict[str, Any]] = None


class BulkNotificationRequest(BaseModel):
    """
    Schema for sending notifications to all users of a type
    """
    user_type: str  # 'instructor' or 'student' 
    title: str
    body: str
    data: Optional[Dict[str, Any]] = None


class NotificationResponse(BaseModel):
    """
    Response after sending notification
    """
    success: bool
    message: str
    message_id: Optional[str] = None
    error: Optional[str] = None


class NotificationLogResponse(BaseModel):
    """
    Response schema for notification log entries
    """
    id: str
    user_id: str
    user_type: str
    title: str
    body: str
    success: bool
    sent_at: datetime

    class Config:
        from_attributes = True