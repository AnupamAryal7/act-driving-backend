from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.courses.models import Course
from app.courses.schemas import Course, CourseCreate, CourseUpdate
from app.courses.services import CourseService


router = APIRouter(tags=["courses"])

@router.get("/", response_model=List[Course])
def get_all_courses(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=200, description="Number of records to return"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """
    Get all courses with optional filtering and pagination.
    """
    return CourseService.get_all_courses(db, skip=skip, limit=limit, is_active=is_active)

@router.get("/active", response_model=List[Course])
def get_active_courses(db: Session = Depends(get_db)):
    """
    Get all active courses.
    """
    return CourseService.get_active_courses(db)

@router.get("/{course_id}", response_model=Course)
def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    """
    Get a specific course by ID.
    """
    return CourseService.get_course_by_id(db, course_id)

@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(course_data: CourseCreate, db: Session = Depends(get_db)):
    """
    Create a new course.
    """
    return CourseService.create_course(db, course_data)

@router.put("/{course_id}", response_model=Course)
def update_course(
    course_id: int, 
    course_data: CourseUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing course.
    """
    return CourseService.update_course(db, course_id, course_data)

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """
    Soft delete a course (sets is_active to false).
    """
    CourseService.delete_course(db, course_id)
    return None

@router.delete("/hard/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def hard_delete_course(course_id: int, db: Session = Depends(get_db)):
    """
    Permanently delete a course from database.
    """
    CourseService.hard_delete_course(db, course_id)
    return None

@router.patch("/{course_id}/restore", response_model=Course)
def restore_course(course_id: int, db: Session = Depends(get_db)):
    """
    Restore a soft-deleted course.
    """
    return CourseService.restore_course(db, course_id)

@router.get("/search/{search_term}", response_model=List[Course])
def search_courses(
    search_term: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Search courses by title or description.
    """
    return CourseService.search_courses(db, search_term, skip=skip, limit=limit)

@router.get("/filter/price", response_model=List[Course])
def filter_courses_by_price(
    min_price: float = Query(..., ge=0, description="Minimum price"),
    max_price: float = Query(..., ge=0, description="Maximum price"),
    is_active: bool = Query(True, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """
    Get courses within a specific price range.
    """
    if min_price > max_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Minimum price cannot be greater than maximum price"
        )
    
    return CourseService.get_courses_by_price_range(
        db, min_price, max_price, is_active
    )

@router.get("/filter/package/{package_type}", response_model=List[Course])
def filter_courses_by_package_type(
    package_type: str,
    is_active: bool = Query(True, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """
    Get courses by package type.
    """
    return CourseService.get_courses_by_package_type(db, package_type, is_active)