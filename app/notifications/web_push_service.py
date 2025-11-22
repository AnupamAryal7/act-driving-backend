"""
Web Push Service using VAPID for sending Firebase push notifications
Handles the actual sending of notifications to FCM
"""
import json
import jwt
import time
from typing import Dict, Any, Optional
import httpx
from pywebpush import webpush, WebPushException
import logging
import os

logger = logging.getLogger(__name__)


class WebPushService:
    """
    Service for sending web push notifications using VAPID authentication
    """
    
    def __init__(self):
        self.vapid_private_key = os.getenv("VAPID_PRIVATE_KEY")
        self.vapid_public_key = os.getenv("VAPID_PUBLIC_KEY") 
        self.vapid_claim_email = os.getenv("VAPID_CLAIM_EMAIL")
        self.fcm_url = "https://fcm.googleapis.com/fcm/send"
        
        # Validate that required environment variables are set
        if not all([self.vapid_private_key, self.vapid_public_key, self.vapid_claim_email]):
            logger.error("Missing VAPID environment variables")
            raise ValueError("VAPID keys and email must be set in environment variables")
    
    def _get_vapid_headers(self, audience: str) -> Dict[str, str]:
        """
        Generate VAPID headers for FCM authentication
        """
        try:
            # VAPID token expires in 12 hours
            exp_time = int(time.time()) + (12 * 60 * 60)
            
            jwt_payload = {
                "aud": audience,
                "exp": exp_time,
                "sub": self.vapid_claim_email
            }
            
            # Create JWT token with VAPID private key
            vapid_token = jwt.encode(
                jwt_payload,
                self.vapid_private_key,
                algorithm="ES256",
                headers={"typ": "JWT"}
            )
            
            return {
                "Authorization": f"vapid t={vapid_token}, k={self.vapid_public_key}",
                "Content-Type": "application/json"
            }
        except Exception as e:
            logger.error(f"Error generating VAPID headers: {str(e)}")
            raise
    
    async def send_push_notification(
        self,
        fcm_token: str,
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a push notification to a single FCM token
        
        Args:
            fcm_token: The FCM device token
            title: Notification title
            body: Notification body
            data: Additional data payload (optional)
            
        Returns:
            Dictionary with success status and response details
        """
        try:
            # Prepare the notification payload
            payload = {
                "title": title,
                "body": body,
            }
            
            if data:
                payload["data"] = data
            
            # FCM endpoint for this specific token
            fcm_endpoint = f"https://fcm.googleapis.com/v1/projects/{os.getenv('FIREBASE_PROJECT_ID')}/messages:send"
            
            # FCM message structure
            message = {
                "message": {
                    "token": fcm_token,
                    "notification": {
                        "title": title,
                        "body": body
                    },
                    "webpush": {
                        "headers": {
                            "Urgency": "normal"
                        }
                    }
                }
            }
            
            # Add data if provided
            if data:
                message["message"]["data"] = data
            
            # Get VAPID headers
            headers = self._get_vapid_headers("https://fcm.googleapis.com")
            
            # Send the request to FCM
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    fcm_endpoint,
                    json=message,
                    headers=headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    logger.info(f"Notification sent successfully: {response_data}")
                    return {
                        "success": True,
                        "message": "Notification sent successfully",
                        "message_id": response_data.get("name")
                    }
                else:
                    error_msg = f"FCM error: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    return {
                        "success": False,
                        "error": error_msg
                    }
                        
        except httpx.RequestError as e:
            error_msg = f"HTTP request error: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
        except Exception as e:
            error_msg = f"Unexpected error sending notification: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }


# Create global instance
web_push_service = WebPushService()