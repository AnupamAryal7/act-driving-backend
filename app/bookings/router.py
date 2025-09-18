from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.bookings.models import Booking
from app.bookings.schemas import Booking, BookingCreate, BookingUpdate
from app.bookings.services import BookingService

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"]
)

# GET endpoints
@router.get("/", response_model=List[Booking])
def get_all_bookings(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=200, description="Number of records to return"),
    student_id: Optional[int] = Query(None, description="Filter by student ID"),
    class_id: Optional[int] = Query(None, description="Filter by class ID"),
    status: Optional[str] = Query(None, description="Filter by booking status"),
    db: Session = Depends(get_db)
):
    """
    Get all bookings with optional filtering.
    """
    try:
        return BookingService.get_all_bookings(
            db, skip=skip, limit=limit, 
            student_id=student_id, 
            class_id=class_id,
            status=status
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching bookings: {str(e)}"
        )

@router.get("/{phone_no}", response_model = List[Booking])
def get_all_bookings_from_phone_no(phone_no: str, db:Session = Depends(get_db)):
    """Get all bookings for a specific phone number"""
    try:
        return BookingService.get_booking_from_phone_no(db, phone_no)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error fetching bookings from phone number: {str(e)}"
        )

@router.get("/student/{student_id}", response_model=List[Booking])
def get_student_bookings(student_id: int, db: Session = Depends(get_db)):
    """
    Get all bookings for a specific student.
    """
    try:
        return BookingService.get_student_bookings(db, student_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching student bookings: {str(e)}"
        )

@router.get("/class/{class_id}", response_model=List[Booking])
def get_class_bookings(class_id: int, db: Session = Depends(get_db)):
    """
    Get all bookings for a specific class.
    """
    try:
        return BookingService.get_class_bookings(db, class_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching class bookings: {str(e)}"
        )

@router.get("/{booking_id}", response_model=Booking)
def get_booking_by_id(booking_id: int, db: Session = Depends(get_db)):
    """
    Get a specific booking by ID.
    """
    try:
        return BookingService.get_booking_by_id(db, booking_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching booking: {str(e)}"
        )

# CREATE endpoint
@router.post("/", response_model=Booking, status_code=status.HTTP_201_CREATED)
def create_booking(booking_data: BookingCreate, db: Session = Depends(get_db)):
    """
    Create a new booking.
    """
    try:
        return BookingService.create_booking(db, booking_data)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating booking: {str(e)}"
        )

# UPDATE endpoints
@router.put("/{booking_id}", response_model=Booking)
def update_booking(
    booking_id: int, 
    booking_data: BookingUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing booking.
    """
    try:
        return BookingService.update_booking(db, booking_id, booking_data)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating booking: {str(e)}"
        )

@router.patch("/{booking_id}/status", response_model=Booking)
def update_booking_status(
    booking_id: int, 
    status: str = Query(..., description="New status: pending, confirmed, cancelled, attended, no_show"),
    db: Session = Depends(get_db)
):
    """
    Update booking status.
    """
    try:
        return BookingService.update_booking_status(db, booking_id, status)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating booking status: {str(e)}"
        )

# DELETE endpoints
@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Permanently delete a booking.
    """
    try:
        BookingService.delete_booking(db, booking_id)
        return None
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting booking: {str(e)}"
        )

@router.delete("/student/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_bookings(student_id: int, db: Session = Depends(get_db)):
    """
    Delete all bookings for a student.
    """
    try:
        BookingService.delete_student_bookings(db, student_id)
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting student bookings: {str(e)}"
        )

@router.delete("/class/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class_bookings(class_id: int, db: Session = Depends(get_db)):
    """
    Delete all bookings for a class.
    """
    try:
        BookingService.delete_class_bookings(db, class_id)
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting class bookings: {str(e)}"
        )