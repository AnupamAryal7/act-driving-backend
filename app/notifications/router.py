"""
Notification Router - API endpoints for push notifications
Handles token registration and notification sending
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database import get_db
from app.notifications.schemas import (
    FCMTokenRegister,
    FCMTokenResponse,
    NotificationRequest,
    BulkNotificationRequest,
    BookingNotificationData,
    ProgressNotificationData,
    NotificationResponse
)
from app.notifications.notification_service import get_notification_service
from app.notifications.web_push_service import web_push_service
from app.bookings.models import Booking
from app.progress_reports.models import ProgressReport

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post(
    "/register-token",
    response_model=FCMTokenResponse,
    summary="Register FCM Token",
    description="Register a new FCM token for push notifications"
)
async def register_fcm_token(
    token_data: FCMTokenRegister,
    db: Session = Depends(get_db)
):
    """
    Register FCM token for a user device
    
    - **user_id**: ID of the user
    - **user_type**: 'instructor' or 'student'  
    - **fcm_token**: FCM device token from browser
    - **device_info**: Optional device information
    """
    try:
        service = get_notification_service(db)
        result = await service.register_fcm_token(
            user_id=token_data.user_id,
            user_type=token_data.user_type,
            fcm_token=token_data.fcm_token,
            device_info=token_data.device_info
        )
        
        if result["success"]:
            return FCMTokenResponse(
                message=result["message"],
                token_id=result["token_id"]
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in register_fcm_token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/send-to-user",
    response_model=NotificationResponse,
    summary="Send Notification to User",
    description="Send push notification to a specific user"
)
async def send_notification_to_user(
    request: NotificationRequest,
    db: Session = Depends(get_db)
):
    """
    Send push notification to a specific user
    
    - **user_id**: Target user ID
    - **title**: Notification title
    - **body**: Notification body
    - **data**: Additional data (optional)
    """
    try:
        service = get_notification_service(db)
        
        # Get user's active tokens
        tokens = service.get_user_tokens(request.user_id)
        
        if not tokens:
            return NotificationResponse(
                success=False,
                message="No active FCM tokens found for user"
            )
        
        # Send to all user's devices
        for token in tokens:
            result = await web_push_service.send_push_notification(
                fcm_token=token.fcm_token,
                title=request.title,
                body=request.body,
                data=request.data
            )
            
            # Log the notification attempt
            service._create_notification_log(
                user_id=request.user_id,
                user_type=token.user_type,
                title=request.title,
                body=request.body,
                fcm_token=token.fcm_token,
                success=result["success"],
                error_message=result.get("error"),
                data=request.data
            )
            
            # If any token succeeds, consider it successful
            if result["success"]:
                return NotificationResponse(
                    success=True,
                    message="Notification sent successfully",
                    message_id=result.get("message_id")
                )
        
        # If all tokens failed
        return NotificationResponse(
            success=False,
            message="Failed to send notification to any device",
            error="All delivery attempts failed"
        )
        
    except Exception as e:
        logger.error(f"Error in send_notification_to_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/send-to-all-instructors",
    response_model=NotificationResponse,
    summary="Send to All Instructors", 
    description="Send push notification to all active instructors"
)
async def send_notification_to_all_instructors(
    request: BulkNotificationRequest,
    db: Session = Depends(get_db)
):
    """
    Send push notification to all active instructors
    
    - **title**: Notification title
    - **body**: Notification body  
    - **data**: Additional data (optional)
    """
    try:
        service = get_notification_service(db)
        
        # Get all instructor tokens
        tokens = service.get_tokens_by_user_type("instructor")
        
        if not tokens:
            return NotificationResponse(
                success=False,
                message="No active instructor tokens found"
            )
        
        success_count = 0
        for token in tokens:
            result = await web_push_service.send_push_notification(
                fcm_token=token.fcm_token,
                title=request.title,
                body=request.body,
                data=request.data
            )
            
            # Log the notification attempt
            service._create_notification_log(
                user_id=token.user_id,
                user_type=token.user_type,
                title=request.title,
                body=request.body,
                fcm_token=token.fcm_token,
                success=result["success"],
                error_message=result.get("error"),
                data=request.data
            )
            
            if result["success"]:
                success_count += 1
        
        return NotificationResponse(
            success=success_count > 0,
            message=f"Notification sent to {success_count} instructors"
        )
        
    except Exception as e:
        logger.error(f"Error in send_notification_to_all_instructors: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/send-to-all-students",
    response_model=NotificationResponse,
    summary="Send to All Students",
    description="Send push notification to all active students"
)
async def send_notification_to_all_students(
    request: BulkNotificationRequest,
    db: Session = Depends(get_db)
):
    """
    Send push notification to all active students
    
    - **title**: Notification title
    - **body**: Notification body  
    - **data**: Additional data (optional)
    """
    try:
        service = get_notification_service(db)
        
        # Get all student tokens
        tokens = service.get_tokens_by_user_type("student")
        
        if not tokens:
            return NotificationResponse(
                success=False,
                message="No active student tokens found"
            )
        
        success_count = 0
        for token in tokens:
            result = await web_push_service.send_push_notification(
                fcm_token=token.fcm_token,
                title=request.title,
                body=request.body,
                data=request.data
            )
            
            # Log the notification attempt
            service._create_notification_log(
                user_id=token.user_id,
                user_type=token.user_type,
                title=request.title,
                body=request.body,
                fcm_token=token.fcm_token,
                success=result["success"],
                error_message=result.get("error"),
                data=request.data
            )
            
            if result["success"]:
                success_count += 1
        
        return NotificationResponse(
            success=success_count > 0,
            message=f"Notification sent to {success_count} students"
        )
        
    except Exception as e:
        logger.error(f"Error in send_notification_to_all_students: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/new-booking",
    response_model=NotificationResponse,
    summary="Notify New Booking",
    description="Send notification to instructors when a new booking is created"
)
async def notify_new_booking(
    booking_data: BookingNotificationData,
    db: Session = Depends(get_db)
):
    """
    Send notification to all instructors about a new booking
    
    - **booking_id**: ID of the new booking
    - **student_name**: Name of the student who made the booking
    - **booking_time**: Optional booking time
    """
    try:
        service = get_notification_service(db)
        
        # Prepare notification content
        title = "New Booking Received"
        body = f"New booking from {booking_data.student_name}"
        
        # Add booking time to body if provided
        if booking_data.booking_time:
            body += f" at {booking_data.booking_time}"
        
        # Prepare data payload
        data = {
            "type": "new_booking",
            "booking_id": booking_data.booking_id,
            "student_name": booking_data.student_name
        }
        
        # Get all instructor tokens
        tokens = service.get_tokens_by_user_type("instructor")
        
        if not tokens:
            return NotificationResponse(
                success=False,
                message="No active instructor tokens found"
            )
        
        success_count = 0
        for token in tokens:
            result = await web_push_service.send_push_notification(
                fcm_token=token.fcm_token,
                title=title,
                body=body,
                data=data
            )
            
            # Log the notification attempt
            service._create_notification_log(
                user_id=token.user_id,
                user_type=token.user_type,
                title=title,
                body=body,
                fcm_token=token.fcm_token,
                success=result["success"],
                error_message=result.get("error"),
                data=data
            )
            
            if result["success"]:
                success_count += 1
        
        return NotificationResponse(
            success=success_count > 0,
            message=f"Booking notification sent to {success_count} instructors"
        )
        
    except Exception as e:
        logger.error(f"Error in notify_new_booking: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/progress-report-updated",
    response_model=NotificationResponse,
    summary="Notify Progress Report Update",
    description="Send notification to student when progress report is updated"
)
async def notify_progress_report_updated(
    progress_data: ProgressNotificationData,
    db: Session = Depends(get_db)
):
    """
    Send notification to student about progress report update
    
    - **progress_id**: ID of the progress report
    - **student_id**: ID of the student to notify
    """
    try:
        service = get_notification_service(db)
        
        # Prepare notification content
        title = "Progress Report Updated"
        body = "Your progress report has been updated. Please have a look."
        
        # Prepare data payload
        data = {
            "type": "progress_report_updated",
            "progress_id": progress_data.progress_id
        }
        
        # Add instructor name if provided
        if progress_data.instructor_name:
            data["instructor_name"] = progress_data.instructor_name
        
        # Get student's active tokens
        tokens = service.get_user_tokens(progress_data.student_id)
        
        if not tokens:
            return NotificationResponse(
                success=False,
                message="No active FCM tokens found for student"
            )
        
        success_count = 0
        for token in tokens:
            result = await web_push_service.send_push_notification(
                fcm_token=token.fcm_token,
                title=title,
                body=body,
                data=data
            )
            
            # Log the notification attempt
            service._create_notification_log(
                user_id=progress_data.student_id,
                user_type="student",
                title=title,
                body=body,
                fcm_token=token.fcm_token,
                success=result["success"],
                error_message=result.get("error"),
                data=data
            )
            
            if result["success"]:
                success_count += 1
        
        return NotificationResponse(
            success=success_count > 0,
            message=f"Progress notification sent to student on {success_count} devices"
        )
        
    except Exception as e:
        logger.error(f"Error in notify_progress_report_updated: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )