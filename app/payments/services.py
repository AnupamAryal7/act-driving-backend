from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.payments.models import Payment, PaymentStatus
from app.payments.schemas import PaymentCreate, PaymentUpdate
from app.auth.users.models import User
from app.courses.models import Course  

class PaymentService:
    
    # GET operations
    @staticmethod
    def get_payment_by_id(db: Session, payment_id: int) -> Payment:
        """Get a single payment by ID"""
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
        return payment

    @staticmethod
    def get_all_payments(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        student_id: Optional[int] = None,
        course_id: Optional[int] = None,
        status: Optional[PaymentStatus] = None
    ) -> List[Payment]:
        """Get all payments with optional filtering"""
        query = db.query(Payment)
        
        if student_id is not None:
            query = query.filter(Payment.student_id == student_id)
            
        if course_id is not None:
            query = query.filter(Payment.course_id == course_id)
            
        if status is not None:
            query = query.filter(Payment.status == status)
            
        return query.order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_student_payments(db: Session, student_id: int) -> List[Payment]:
        """Get all payments for a specific student"""
        return db.query(Payment).filter(Payment.student_id == student_id).all()

    @staticmethod
    def get_course_payments(db: Session, course_id: int) -> List[Payment]:
        """Get all payments for a specific course"""
        return db.query(Payment).filter(Payment.course_id == course_id).all()

    @staticmethod
    def get_payments_by_status(db: Session, status: PaymentStatus) -> List[Payment]:
        """Get all payments with specific status"""
        return db.query(Payment).filter(Payment.status == status).all()

    # CREATE operation
    @staticmethod
    def create_payment(db: Session, payment_data: PaymentCreate) -> Payment:
        """Create a new payment with validation"""
        # Validate student exists
        student = db.query(User).filter(User.id == payment_data.student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student not found"
            )
        
        # Validate course exists
        course = db.query(Course).filter(Course.id == payment_data.course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course not found"
            )
        
        # Validate amount is positive
        if payment_data.amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment amount must be positive"
            )
        
        # Check if transaction_id already exists (if provided)
        if payment_data.transaction_id:
            existing_payment = db.query(Payment).filter(
                Payment.transaction_id == payment_data.transaction_id
            ).first()
            if existing_payment:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Transaction ID already exists"
                )
        
        # Create payment
        db_payment = Payment(
            student_id=payment_data.student_id,
            course_id=payment_data.course_id,
            amount=payment_data.amount,
            status=payment_data.status,
            payment_method=payment_data.payment_method,
            transaction_id=payment_data.transaction_id
        )
        
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        return db_payment

    # UPDATE operations
    @staticmethod
    def update_payment(db: Session, payment_id: int, payment_data: PaymentUpdate) -> Payment:
        """Update an existing payment"""
        payment = PaymentService.get_payment_by_id(db, payment_id)
        
        update_data = payment_data.model_dump(exclude_unset=True)
        
        # Check if new transaction_id already exists
        if 'transaction_id' in update_data and update_data['transaction_id']:
            existing_payment = db.query(Payment).filter(
                Payment.transaction_id == update_data['transaction_id'],
                Payment.id != payment_id
            ).first()
            if existing_payment:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Transaction ID already exists"
                )
        
        for field, value in update_data.items():
            setattr(payment, field, value)
            
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def update_payment_status(db: Session, payment_id: int, status: PaymentStatus) -> Payment:
        """Update only the payment status"""
        payment = PaymentService.get_payment_by_id(db, payment_id)
        payment.status = status
        db.commit()
        db.refresh(payment)
        return payment

    # DELETE operations
    @staticmethod
    def delete_payment(db: Session, payment_id: int) -> None:
        """Delete a payment"""
        payment = PaymentService.get_payment_by_id(db, payment_id)
        db.delete(payment)
        db.commit()

    @staticmethod
    def delete_student_payments(db: Session, student_id: int) -> None:
        """Delete all payments for a student"""
        db.query(Payment).filter(Payment.student_id == student_id).delete()
        db.commit()

    @staticmethod
    def delete_course_payments(db: Session, course_id: int) -> None:
        """Delete all payments for a course"""
        db.query(Payment).filter(Payment.course_id == course_id).delete()
        db.commit()

# Utility function
def get_payment_service():
    return PaymentService