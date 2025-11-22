"""
Notification Service - Handles business logic for notifications
Coordinates between database, web push service, and logging
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import logging
from app.notifications.models import UserFCMToken, NotificationLog
from app.notifications.web_push_service import web_push_service
from app.notifications.schemas import NotificationResponse

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service layer for notification operations
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def register_fcm_token(
        self, 
        user_id: str, 
        user_type: str, 
        fcm_token: str, 
        device_info: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register or update FCM token for a user
        
        Args:
            user_id: ID of the user
            user_type: 'instructor' or 'student'
            fcm_token: FCM device token
            device_info: Optional device information
            
        Returns:
            Dictionary with registration result
        """
        try:
            # Check if token already exists
            existing_token = self.db.query(UserFCMToken).filter(
                UserFCMToken.fcm_token == fcm_token
            ).first()
            
            if existing_token:
                # Update existing token with new user info
                existing_token.user_id = user_id
                existing_token.user_type = user_type
                existing_token.device_info = device_info
                existing_token.is_active = True
                token_id = existing_token.id
            else:
                # Create new token record
                new_token = UserFCMToken(
                    user_id=user_id,
                    user_type=user_type,
                    fcm_token=fcm_token,
                    device_info=device_info
                )
                self.db.add(new_token)
                self.db.flush()  # Get the ID without committing
                token_id = new_token.id
            
            self.db.commit()
            
            logger.info(f"FCM token registered for user {user_id}")
            return {
                "success": True,
                "message": "FCM token registered successfully",
                "token_id": token_id
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error registering FCM token: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to register token: {str(e)}"
            }
    
    def _create_notification_log(
        self,
        user_id: str,
        user_type: str,
        title: str,
        body: str,
        fcm_token: str,
        success: bool,
        error_message: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Create a log entry for notification attempt
        
        Args:
            user_id: ID of the target user
            user_type: 'instructor' or 'student'
            title: Notification title
            body: Notification body
            fcm_token: FCM token used
            success: Whether notification was successful
            error_message: Error message if failed
            data: Additional data sent with notification
        """
        try:
            log_entry = NotificationLog(
                user_id=user_id,
                user_type=user_type,
                title=title,
                body=body,
                data=data,
                fcm_token=fcm_token,
                success=success,
                error_message=error_message
            )
            self.db.add(log_entry)
            self.db.commit()
        except Exception as e:
            logger.error(f"Failed to create notification log: {str(e)}")
            self.db.rollback()
    
    def get_user_tokens(self, user_id: str) -> List[UserFCMToken]:
        """
        Get all active FCM tokens for a user
        
        Args:
            user_id: ID of the user
            
        Returns:
            List of active FCM tokens
        """
        return self.db.query(UserFCMToken).filter(
            UserFCMToken.user_id == user_id,
            UserFCMToken.is_active == True
        ).all()
    
    def get_tokens_by_user_type(self, user_type: str) -> List[UserFCMToken]:
        """
        Get all active FCM tokens for a user type
        
        Args:
            user_type: 'instructor' or 'student'
            
        Returns:
            List of active FCM tokens
        """
        return self.db.query(UserFCMToken).filter(
            UserFCMToken.user_type == user_type,
            UserFCMToken.is_active == True
        ).all()


# Utility function to create service instance
def get_notification_service(db: Session) -> NotificationService:
    """
    Factory function to create NotificationService instance
    """
    return NotificationService(db)