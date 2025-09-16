from cloudinary.uploader import upload, destroy
from fastapi import HTTPException, status
import io

class CloudinaryService:
    @staticmethod
    async def upload_course_image(image_file, course_id: int):
        try:
            content = await image_file.read()
            
            result = upload(
                io.BytesIO(content),
                folder=f"courses/{course_id}",
                transformation=[
                    {'width': 1200, 'height': 800, 'crop': 'limit'},
                    {'quality': 'auto'},
                    {'format': 'auto'}
                ]
            )
            
            return {
                "url": result.get('secure_url'),
                "public_id": result.get('public_id')
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image upload failed: {str(e)}"
            )

    @staticmethod
    def delete_image(public_id: str):
        try:
            destroy(public_id)
            return True
        except Exception:
            return False