from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, text
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from typing import List, Optional

from app.class_sessions.models import ClassSession
from app.class_sessions.schemas import ClassSessionCreate, ClassSessionUpdate
from app.auth.users.models import User
from app.courses.models import Course

class ClassSessionService:
    
    # GET operations
    @staticmethod
    def get_session_by_id(db: Session, session_id: int) -> ClassSession:
        session = db.query(ClassSession).filter(ClassSession.id == session_id).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class session not found"
            )
        return session

    @staticmethod
    def get_all_sessions(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        course_id: Optional[int] = None,
        instructor_id: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> List[ClassSession]:
        query = db.query(ClassSession)
        
        if course_id is not None:
            query = query.filter(ClassSession.course_id == course_id)
            
        if instructor_id is not None:
            query = query.filter(ClassSession.instructor_id == instructor_id)
            
        if is_active is not None:
            query = query.filter(ClassSession.is_active == is_active)
            
        return query.order_by(ClassSession.date_time).offset(skip).limit(limit).all()

    @staticmethod
    def get_upcoming_sessions(db: Session, hours_ahead: int = 24) -> List[ClassSession]:
        now = datetime.now()
        future_time = now + timedelta(hours=hours_ahead)
        
        return db.query(ClassSession).filter(
            and_(
                ClassSession.date_time >= now,
                ClassSession.date_time <= future_time,
                ClassSession.is_active == True
            )
        ).order_by(ClassSession.date_time).all()

    # CREATE operation
    @staticmethod
    def create_session(db: Session, session_data: ClassSessionCreate) -> ClassSession:
        # Validate instructor role
        # instructor = db.query(User).filter(User.id == session_data.instructor_id).first()
        # if not instructor or instructor.role != "instructor":
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="User must be an instructor to create class sessions"
        #     )
        
        # Validate course exists
        course = db.query(Course).filter(Course.id == session_data.course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course not found"
            )
        
        # Check for time conflicts
        ClassSessionService._check_time_conflict(db, session_data)
        
        # Create session
        db_session = ClassSession(
            course_id=session_data.course_id,
            instructor_id=session_data.instructor_id,
            date_time=session_data.date_time,
            duration=session_data.duration,
            is_active=session_data.is_active
        )
        
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session

    # UPDATE operations
    @staticmethod
    def update_session(db: Session, session_id: int, session_data: ClassSessionUpdate) -> ClassSession:
        session = ClassSessionService.get_session_by_id(db, session_id)
        
        update_data = session_data.model_dump(exclude_unset=True)
        
        # If updating time/duration, check for conflicts
        if 'date_time' in update_data or 'duration' in update_data:
            check_data = ClassSessionCreate(
                course_id=session.course_id,
                instructor_id=session.instructor_id,
                date_time=update_data.get('date_time', session.date_time),
                duration=update_data.get('duration', session.duration),
                is_active=session.is_active
            )
            ClassSessionService._check_time_conflict(db, check_data)
        
        for field, value in update_data.items():
            setattr(session, field, value)
            
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def cancel_session(db: Session, session_id: int) -> ClassSession:
        session = ClassSessionService.get_session_by_id(db, session_id)
        session.is_active = False
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def activate_session(db: Session, session_id: int) -> ClassSession:
        session = ClassSessionService.get_session_by_id(db, session_id)
        session.is_active = True
        db.commit()
        db.refresh(session)
        return session

    # DELETE operations
    @staticmethod
    def delete_session(db: Session, session_id: int) -> None:
        session = ClassSessionService.get_session_by_id(db, session_id)
        db.delete(session)
        db.commit()

    @staticmethod
    def delete_course_sessions(db: Session, course_id: int) -> None:
        db.query(ClassSession).filter(ClassSession.course_id == course_id).delete()
        db.commit()

    @staticmethod
    def delete_instructor_sessions(db: Session, instructor_id: int) -> None:
        db.query(ClassSession).filter(ClassSession.instructor_id == instructor_id).delete()
        db.commit()

    @staticmethod
    def _check_time_conflict(db: Session, session_data: ClassSessionCreate):
        session_start = session_data.date_time
        # FIX: duration is in MINUTES, not hours
        session_end = session_start + timedelta(minutes=session_data.duration)
        
        # Use PostgreSQL interval functions for accurate time calculation
        conflicting_sessions = db.query(ClassSession).filter(
            and_(
                ClassSession.instructor_id == session_data.instructor_id,
                ClassSession.is_active == True,
                # Check for time overlap using database interval arithmetic
                # FIX: duration is stored in minutes, so use '1 minute' not '1 hour'
                ClassSession.date_time < session_end,
                ClassSession.date_time + text("interval '1 minute' * duration") > session_start
            )
        ).first()
        
        if conflicting_sessions:
            conflict_start = conflicting_sessions.date_time
            # FIX: duration is in minutes
            conflict_end = conflict_start + timedelta(minutes=conflicting_sessions.duration)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Instructor already has a class from {conflict_start} to {conflict_end}"
            )
    
# Utility function
def get_class_session_service():
    return ClassSessionService