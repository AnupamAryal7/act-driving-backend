from fastapi import APIRouter, Depends, status, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.database import get_db
from app.courses.models import Course
from app.courses.schemas import Course, CourseCreate, CourseUpdate, ImageUploadResponse
from app.courses.services import CourseService

# add router
router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)

@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_title: str = Form(..., max_length=50),
    description: str = Form(...),
    bullet_pt1: str = Form(..., max_length=80),
    bullet_pt2: str = Form(..., max_length=80),
    bullet_pt3: str = Form(..., max_length=80),
    duration: str = Form(..., max_length=25),
    package_type: str = Form(..., max_length=20),
    total_price: float = Form(...),
    discounted_price: Optional[float] = Form(None),
    is_active: bool = Form(True),
    image: UploadFile = File(..., description="Course image file (JPEG, PNG, WebP) - REQUIRED"),
    db: Session = Depends(get_db)
):
    """Create a course with mandatory image upload"""
    try:
        # Validate image (now mandatory)
        allowed_types = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
        if image.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only JPEG, PNG, and WebP images are allowed"
            )
        
        if image.size > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image size must be less than 5MB"
            )
        
        # Create course data object
        course_data = CourseCreate(
            course_title=course_title,
            description=description,
            bullet_pt1=bullet_pt1,
            bullet_pt2=bullet_pt2,
            bullet_pt3=bullet_pt3,
            duration=duration,
            package_type=package_type,
            total_price=total_price,
            discounted_price=discounted_price,
            is_active=is_active
        )
        
        return await CourseService.create_course_with_image(db, course_data, image)
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating course: {str(e)}"
        )

@router.get("/", response_model=List[Course])
def get_all_courses(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=200, description="Number of records to return"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    # get all courses with optional filtering by active status
    try:
        return CourseService.get_all_courses(db, skip, limit, is_active)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching courses: {str(e)}"
        )

@router.get("/active", response_model=List[Course])
def get_active_courses(db: Session = Depends(get_db)):
    # get all active courses
    try:
        return CourseService.get_active_courses(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching active courses: {str(e)}"
        )

@router.get("/{course_id}", response_model=Course)
def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    # get course by id
    try:
        return CourseService.get_course_by_id(db, course_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching course by id: {str(e)}"
        )

@router.put("/{course_id}", response_model=Course)
def update_course(course_id: int, course_data: CourseUpdate, db: Session = Depends(get_db)):
    # update an existing course
    try:
        return CourseService.update_course(db, course_id, course_data)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating course: {str(e)}"
        )

@router.post("/{course_id}/image", response_model=Course)
async def upload_course_image(
    course_id: int,
    image: UploadFile = File(..., description="Course image file (JPEG, PNG, WebP)"),
    db: Session = Depends(get_db)
):
    """Upload or update course image"""
    try:
        # Validate file type
        allowed_types = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
        if image.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only JPEG, PNG, and WebP images are allowed"
            )
        
        # Validate file size (5MB max)
        if image.size > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image size must be less than 5MB"
            )
        
        return await CourseService.update_course_image(db, course_id, image)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading course image: {str(e)}"
        )

@router.delete("/{course_id}/image", response_model=Course)
def delete_course_image(course_id: int, db: Session = Depends(get_db)):
    """Delete course image"""
    try:
        return CourseService.delete_course_image(db, course_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting course image: {str(e)}"
        )

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    # soft delete a course (sets is_active to false)
    try:
        CourseService.delete_course(db, course_id)
        return None
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting course: {str(e)}"
        )

@router.delete("/hard/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def hard_delete_course(course_id: int, db: Session = Depends(get_db)):
    # permanently delete a course from database
    try:
        CourseService.hard_delete_course(db, course_id)
        return None
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error hard deleting course: {str(e)}"
        )

@router.patch("/{course_id}/restore", response_model=Course)
def restore_course(course_id: int, db: Session = Depends(get_db)):
    # restore a soft-deleted course
    try:
        return CourseService.restore_course_by_id(db, course_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error restoring course: {str(e)}"
        )

@router.get("/search/{search_term}", response_model=List[Course])
def search_courses(
    search_term: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    # search courses by title or description
    try:
        return CourseService.search_courses(db, search_term, skip, limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching courses: {str(e)}"
        )

@router.get("/filter/price", response_model=List[Course])
def filter_courses_by_price(
    min_price: float = Query(..., ge=0, description="Minimum price"),
    max_price: float = Query(..., ge=0, description="Maximum price"),
    is_active: bool = Query(True, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    # get courses within a specific price range
    try:
        if min_price > max_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum price cannot be greater than maximum price"
            )
        
        return CourseService.get_courses_by_price_range(db, min_price, max_price, is_active)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error filtering courses by price: {str(e)}"
        )

@router.get("/filter/package/{package_type}", response_model=List[Course])
def filter_courses_by_package_type(
    package_type: str,
    is_active: bool = Query(True, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    # get courses by package type
    try:
        return CourseService.get_courses_by_package_type(db, package_type, is_active)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error filtering courses by package type: {str(e)}"
        )