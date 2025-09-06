from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.class_sessions.models import ClassSession
from app.class_sessions.schemas import ClassSession, ClassSessionCreate, ClassSessionUpdate
from app.class_sessions.services import ClassSessionService

router = APIRouter(
    prefix="/class_sessions",
    tags=["class_sessions"]
)

# GET endpoints
@router.get("/", response_model=List[ClassSession])
def get_all_class_sessions(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=200, description="Number of records to return"),
    course_id: Optional[int] = Query(None, description="Filter by course ID"),
    instructor_id: Optional[int] = Query(None, description="Filter by instructor ID"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """
    Get all class sessions with optional filtering.
    """
    try:
        return ClassSessionService.get_all_sessions(
            db, skip=skip, limit=limit, 
            course_id=course_id, 
            instructor_id=instructor_id,
            is_active=is_active
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching class sessions: {str(e)}"
        )

@router.get("/upcoming", response_model=List[ClassSession])
def get_upcoming_sessions(
    hours_ahead: int = Query(24, ge=1, le=168, description="Hours to look ahead (1-168)"),
    db: Session = Depends(get_db)
):
    """
    Get class sessions happening in the next specified hours.
    """
    try:
        return ClassSessionService.get_upcoming_sessions(db, hours_ahead=hours_ahead)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching upcoming sessions: {str(e)}"
        )

@router.get("/{session_id}", response_model=ClassSession)
def get_class_session_by_id(session_id: int, db: Session = Depends(get_db)):
    """
    Get a specific class session by ID.
    """
    try:
        return ClassSessionService.get_session_by_id(db, session_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching class session: {str(e)}"
        )

# CREATE endpoint
@router.post("/", response_model=ClassSession, status_code=status.HTTP_201_CREATED)
def create_class_session(session_data: ClassSessionCreate, db: Session = Depends(get_db)):
    """
    Create a new class session.
    """
    try:
        return ClassSessionService.create_session(db, session_data)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating class session: {str(e)}"
        )

# UPDATE endpoints
@router.put("/{session_id}", response_model=ClassSession)
def update_class_session(
    session_id: int, 
    session_data: ClassSessionUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing class session.
    """
    try:
        return ClassSessionService.update_session(db, session_id, session_data)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating class session: {str(e)}"
        )

@router.patch("/{session_id}/cancel", response_model=ClassSession)
def cancel_class_session(session_id: int, db: Session = Depends(get_db)):
    """
    Cancel a class session (soft delete).
    """
    try:
        return ClassSessionService.cancel_session(db, session_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error canceling class session: {str(e)}"
        )

@router.patch("/{session_id}/activate", response_model=ClassSession)
def activate_class_session(session_id: int, db: Session = Depends(get_db)):
    """
    Reactivate a cancelled class session.
    """
    try:
        return ClassSessionService.activate_session(db, session_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error activating class session: {str(e)}"
        )

# DELETE endpoints
@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class_session(session_id: int, db: Session = Depends(get_db)):
    """
    Permanently delete a class session.
    """
    try:
        ClassSessionService.delete_session(db, session_id)
        return None
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting class session: {str(e)}"
        )

@router.delete("/course/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course_sessions(course_id: int, db: Session = Depends(get_db)):
    """
    Delete all class sessions for a course.
    """
    try:
        ClassSessionService.delete_course_sessions(db, course_id)
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting course sessions: {str(e)}"
        )

@router.delete("/instructor/{instructor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_instructor_sessions(instructor_id: int, db: Session = Depends(get_db)):
    """
    Delete all class sessions for an instructor.
    """
    try:
        ClassSessionService.delete_instructor_sessions(db, instructor_id)
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting instructor sessions: {str(e)}"
        )