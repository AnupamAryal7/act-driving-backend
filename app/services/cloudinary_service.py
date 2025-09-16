from cloudinary.uploader import upload, destroy
from fastapi import HTTPException, status, UploadFile
import io
import logging

logger = logging.getLogger(__name__)

class CloudinaryService:
    @staticmethod
    async def upload_course_image(image_file: UploadFile, course_id: int):
        """
        Upload course image to Cloudinary
        
        Args:
            image_file: The uploaded image file
            course_id: The ID of the course
            
        Returns:
            dict: Contains 'url' and 'public_id' of the uploaded image
        """
        try:
            # Read file content
            content = await image_file.read()
            
            # Reset file pointer for potential reuse
            await image_file.seek(0)
            
            # Upload to Cloudinary
            result = upload(
                io.BytesIO(content),
                folder=f"courses/{course_id}",
                public_id=f"course_{course_id}_{image_file.filename.split('.')[0]}",
                transformation=[
                    {'width': 1200, 'height': 800, 'crop': 'limit'},
                    {'quality': 'auto:good'},
                    {'format': 'auto'}
                ],
                overwrite=True,  # Allow overwriting existing images
                invalidate=True  # Invalidate cached versions
            )
            
            return {
                "url": result.get('secure_url'),
                "public_id": result.get('public_id')
            }
            
        except Exception as e:
            logger.error(f"Cloudinary upload error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image upload failed: {str(e)}"
            )

    @staticmethod
    def delete_image(public_id: str):
        """
        Delete image from Cloudinary
        
        Args:
            public_id: The public ID of the image to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            result = destroy(public_id)
            return result.get('result') == 'ok'
        except Exception as e:
            logger.error(f"Cloudinary delete error: {str(e)}")
            return False

    @staticmethod
    def get_image_url_with_transformations(public_id: str, width: int = None, height: int = None, quality: str = "auto"):
        """
        Generate Cloudinary URL with custom transformations
        
        Args:
            public_id: The public ID of the image
            width: Desired width
            height: Desired height
            quality: Image quality
            
        Returns:
            str: Transformed image URL
        """
        try:
            from cloudinary import CloudinaryImage
            
            transformations = []
            if width and height:
                transformations.append({'width': width, 'height': height, 'crop': 'fill'})
            elif width:
                transformations.append({'width': width, 'crop': 'scale'})
            elif height:
                transformations.append({'height': height, 'crop': 'scale'})
            
            transformations.append({'quality': quality, 'format': 'auto'})
            
            return CloudinaryImage(public_id).build_url(transformation=transformations)
        except Exception as e:
            logger.error(f"Error generating transformed URL: {str(e)}")
            return None