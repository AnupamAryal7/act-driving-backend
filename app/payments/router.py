from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.payments.models import Payment, PaymentStatus
from app.payments.schemas import Payment, PaymentCreate, PaymentUpdate
from app.payments.services import PaymentService

router = APIRouter(
    tags=["payments"]
)

# GET endpoints
@router.get("/", response_model=List[Payment])
def get_all_payments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=200, description="Number of records to return"),
    student_id: Optional[int] = Query(None, description="Filter by student ID"),
    course_id: Optional[int] = Query(None, description="Filter by course ID"),
    status: Optional[PaymentStatus] = Query(None, description="Filter by payment status"),
    db: Session = Depends(get_db)
):
    """
    Get all payments with optional filtering.
    """
    try:
        return PaymentService.get_all_payments(
            db, skip=skip, limit=limit, 
            student_id=student_id, 
            course_id=course_id,
            status=status
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching payments: {str(e)}"
        )

@router.get("/student/{student_id}", response_model=List[Payment])
def get_student_payments(student_id: int, db: Session = Depends(get_db)):
    """
    Get all payments for a specific student.
    """
    try:
        return PaymentService.get_student_payments(db, student_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching student payments: {str(e)}"
        )

@router.get("/course/{course_id}", response_model=List[Payment])
def get_course_payments(course_id: int, db: Session = Depends(get_db)):
    """
    Get all payments for a specific course.
    """
    try:
        return PaymentService.get_course_payments(db, course_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching course payments: {str(e)}"
        )

@router.get("/status/{status}", response_model=List[Payment])
def get_payments_by_status(status: PaymentStatus, db: Session = Depends(get_db)):
    """
    Get all payments with specific status.
    """
    try:
        return PaymentService.get_payments_by_status(db, status)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching payments by status: {str(e)}"
        )

@router.get("/{payment_id}", response_model=Payment)
def get_payment_by_id(payment_id: int, db: Session = Depends(get_db)):
    """
    Get a specific payment by ID.
    """
    try:
        return PaymentService.get_payment_by_id(db, payment_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching payment: {str(e)}"
        )

# CREATE endpoint
@router.post("/", response_model=Payment, status_code=status.HTTP_201_CREATED)
def create_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    """
    Create a new payment.
    """
    try:
        return PaymentService.create_payment(db, payment_data)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating payment: {str(e)}"
        )

# UPDATE endpoints
@router.put("/{payment_id}", response_model=Payment)
def update_payment(
    payment_id: int, 
    payment_data: PaymentUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing payment.
    """
    try:
        return PaymentService.update_payment(db, payment_id, payment_data)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating payment: {str(e)}"
        )

@router.patch("/{payment_id}/status", response_model=Payment)
def update_payment_status(
    payment_id: int, 
    status: PaymentStatus = Query(..., description="New payment status"),
    db: Session = Depends(get_db)
):
    """
    Update payment status.
    """
    try:
        return PaymentService.update_payment_status(db, payment_id, status)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating payment status: {str(e)}"
        )

# DELETE endpoints
@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    """
    Permanently delete a payment.
    """
    try:
        PaymentService.delete_payment(db, payment_id)
        return None
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting payment: {str(e)}"
        )

@router.delete("/student/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_payments(student_id: int, db: Session = Depends(get_db)):
    """
    Delete all payments for a student.
    """
    try:
        PaymentService.delete_student_payments(db, student_id)
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting student payments: {str(e)}"
        )

@router.delete("/course/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course_payments(course_id: int, db: Session = Depends(get_db)):
    """
    Delete all payments for a course.
    """
    try:
        PaymentService.delete_course_payments(db, course_id)
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting course payments: {str(e)}"
        )