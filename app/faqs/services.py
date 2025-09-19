from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from typing import List, Optional

from app.faqs.models import FAQ
from app.faqs.schemas import FAQCreate, FAQUpdate
from app.faq_categories.models import Faq_Category

class FAQService:

    @staticmethod
    def get_all_faqs(db: Session, category_id: Optional[int] = None) -> List[FAQ]:
        """Get all FAQs, optionally filtered by category"""
        try:
            query = db.query(FAQ)
            if category_id:
                query = query.filter(FAQ.category_id == category_id)
            return query.order_by(FAQ.created_at.desc()).all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching FAQs: {str(e)}"
            )

    @staticmethod
    def get_faq_by_id(db: Session, faq_id: int) -> Optional[FAQ]:
        """Get FAQ by ID"""
        try:
            return db.query(FAQ).filter(FAQ.id == faq_id).first()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching FAQ: {str(e)}"
            )

    @staticmethod
    def create_faq(db: Session, faq_data: FAQCreate) -> FAQ:
        """Create a new FAQ"""
        # Check if category exists
        category = db.query(Faq_Category).filter(Faq_Category.id == faq_data.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {faq_data.category_id} not found"
            )

        try:
            faq = FAQ(
                category_id=faq_data.category_id,
                question=faq_data.question,
                answer=faq_data.answer
            )
            db.add(faq)
            db.commit()
            db.refresh(faq)
            return faq
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while creating FAQ: {str(e)}"
            )

    @staticmethod
    def update_faq(db: Session, faq_id: int, faq_data: FAQUpdate) -> Optional[FAQ]:
        """Update an existing FAQ"""
        faq = FAQService.get_faq_by_id(db, faq_id)
        if not faq:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"FAQ with ID {faq_id} not found"
            )

        # Check if new category exists (if provided)
        if faq_data.category_id is not None:
            category = db.query(Faq_Category).filter(Faq_Category.id == faq_data.category_id).first()
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with ID {faq_data.category_id} not found"
                )

        try:
            if faq_data.category_id is not None:
                faq.category_id = faq_data.category_id
            if faq_data.question is not None:
                faq.question = faq_data.question
            if faq_data.answer is not None:
                faq.answer = faq_data.answer
            
            db.commit()
            db.refresh(faq)
            return faq
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while updating FAQ: {str(e)}"
            )

    @staticmethod
    def delete_faq(db: Session, faq_id: int) -> bool:
        """Delete a FAQ"""
        faq = FAQService.get_faq_by_id(db, faq_id)
        if not faq:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"FAQ with ID {faq_id} not found"
            )

        try:
            db.delete(faq)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while deleting FAQ: {str(e)}"
            )