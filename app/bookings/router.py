from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.bookings.schemas import BookingResponse, BookingCreate, BookingUpdate
from app.bookings import services

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.get("/", response_model=List[BookingResponse])
def get_all_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all bookings with pagination"""
    bookings = services.get_all_bookings(db, skip=skip, limit=limit)
    return bookings

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """Get a specific booking by ID"""
    booking = services.get_booking_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.get("/user/{user_email}", response_model=List[BookingResponse])
def get_bookings_by_user(
    user_email: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get bookings for a specific user"""
    bookings = services.get_bookings_by_user(db, user_email, skip=skip, limit=limit)
    return bookings

@router.get("/status/{status}", response_model=List[BookingResponse])
def get_bookings_by_status(
    status: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get bookings by status (pending, confirmed, cancelled)"""
    valid_statuses = ["pending", "confirmed", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    bookings = services.get_bookings_by_status(db, status, skip=skip, limit=limit)
    return bookings

@router.post("/", response_model=BookingResponse, status_code=201)
def add_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    """Create a new booking"""
    if booking.discount_price and booking.discount_price >= booking.original_price:
        raise HTTPException(
            status_code=400, 
            detail="Discount price must be less than original price"
        )
    return services.add_booking(db, booking)

@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking_id: int, 
    booking_update: BookingUpdate, 
    db: Session = Depends(get_db)
):
    """Update an existing booking"""
    if (booking_update.discount_price is not None and 
        booking_update.original_price is not None and
        booking_update.discount_price >= booking_update.original_price):
        raise HTTPException(
            status_code=400, 
            detail="Discount price must be less than original price"
        )
    
    updated_booking = services.update_booking(db, booking_id, booking_update)
    if not updated_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated_booking

@router.delete("/{booking_id}", status_code=204)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """Delete a booking"""
    success = services.delete_booking(db, booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found")
