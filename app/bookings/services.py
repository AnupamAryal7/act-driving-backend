from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status
from typing import List, Optional

from app.bookings.models import Booking
from app.bookings.schemas import BookingCreate, BookingUpdate
from app.class_sessions.models import ClassSession 
from app.auth.users.models import User 

class BookingService:
    
    # GET operations
    @staticmethod
    def get_booking_by_id(db: Session, booking_id: int) -> Booking:
        """Get a single booking by ID"""
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        return booking

    @staticmethod
    def get_all_bookings(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        student_id: Optional[int] = None,
        class_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Booking]:
        """Get all bookings with optional filtering"""
        query = db.query(Booking)
        
        if student_id is not None:
            query = query.filter(Booking.student_id == student_id)
            
        if class_id is not None:
            query = query.filter(Booking.class_id == class_id)
            
        if status is not None:
            query = query.filter(Booking.status == status)
            
        return query.order_by(Booking.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_student_bookings(db: Session, student_id: int) -> List[Booking]:
        """Get all bookings for a specific student"""
        return db.query(Booking).filter(Booking.student_id == student_id).all()

    @staticmethod
    def get_class_bookings(db: Session, class_id: int) -> List[Booking]:
        """Get all bookings for a specific class"""
        return db.query(Booking).filter(Booking.class_id == class_id).all()
    
    @staticmethod
    def get_booking_from_phone_no(db: Session, phone_no: str) -> List[Booking]:
        """Get all bookings for a phone number"""
        return db.query(Booking).filter(Booking.phone_no == phone_no).all()

    # CREATE operation
    @staticmethod
    def create_booking(db: Session, booking_data: BookingCreate) -> Booking:
        """Create a new booking with validation"""
        # Validate student exists
        student = db.query(User).filter(User.id == booking_data.student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student not found"
            )
        
        # Validate class exists
        class_session = db.query(ClassSession).filter(ClassSession.id == booking_data.class_id).first()
        if not class_session:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Class session not found"
            )
        
        # Check if student already booked this class
        existing_booking = db.query(Booking).filter(
            and_(
                Booking.student_id == booking_data.student_id,
                Booking.class_id == booking_data.class_id
            )
        ).first()
        
        if existing_booking:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student already booked this class"
            )
        
        # Create booking
        db_booking = Booking(
            student_id=booking_data.student_id,
            class_id=booking_data.class_id,
            phone_no = booking_data.phone_no,
            subrub= booking_data.subrub,
            status=booking_data.status,
            remarks=booking_data.remarks
        )
        
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return db_booking

    # UPDATE operations
    @staticmethod
    def update_booking(db: Session, booking_id: int, booking_data: BookingUpdate) -> Booking:
        """Update an existing booking"""
        booking = BookingService.get_booking_by_id(db, booking_id)
        
        update_data = booking_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(booking, field, value)
            
        db.commit()
        db.refresh(booking)
        return booking

    @staticmethod
    def update_booking_status(db: Session, booking_id: int, status: str) -> Booking:
        """Update only the booking status"""
        booking = BookingService.get_booking_by_id(db, booking_id)
        booking.status = status
        db.commit()
        db.refresh(booking)
        return booking

    # DELETE operations
    @staticmethod
    def delete_booking(db: Session, booking_id: int) -> None:
        """Delete a booking"""
        booking = BookingService.get_booking_by_id(db, booking_id)
        db.delete(booking)
        db.commit()

    @staticmethod
    def delete_student_bookings(db: Session, student_id: int) -> None:
        """Delete all bookings for a student"""
        db.query(Booking).filter(Booking.student_id == student_id).delete()
        db.commit()

    @staticmethod
    def delete_class_bookings(db: Session, class_id: int) -> None:
        """Delete all bookings for a class"""
        db.query(Booking).filter(Booking.class_id == class_id).delete()
        db.commit()

# Utility function  
def get_booking_service():
    return BookingService