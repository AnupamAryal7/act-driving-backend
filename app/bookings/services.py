from sqlalchemy.orm import Session
from app.bookings.models import Booking
from app.bookings.schemas import BookingCreate, BookingUpdate
from typing import List, Optional

def get_all_bookings(db: Session, skip: int = 0, limit: int = 100) -> List[Booking]:
    return db.query(Booking).offset(skip).limit(limit).all()

def get_booking_by_id(db: Session, booking_id: int) -> Optional[Booking]:
    return db.query(Booking).filter(Booking.id == booking_id).first()

def get_bookings_by_user(db: Session, user_email: str, skip: int = 0, limit: int = 100) -> List[Booking]:
    return db.query(Booking).filter(Booking.user_email == user_email).offset(skip).limit(limit).all()

def get_bookings_by_status(db: Session, status: str, skip: int = 0, limit: int = 100) -> List[Booking]:
    return db.query(Booking).filter(Booking.booking_status == status).offset(skip).limit(limit).all()

def add_booking(db: Session, booking: BookingCreate) -> Booking:
    db_booking = Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def update_booking(db: Session, booking_id: int, booking_update: BookingUpdate) -> Optional[Booking]:
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if db_booking:
        update_data = booking_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_booking, field, value)
        db.commit()
        db.refresh(db_booking)
    return db_booking

def delete_booking(db: Session, booking_id: int) -> bool:
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if db_booking:
        db.delete(db_booking)
        db.commit()
        return True
    return False