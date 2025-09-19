from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from typing import List, Optional

from app.faq_categories.schemas import Faq_Category


class Faq_Category_Service:

    @staticmethod
    def get_category_by_id(db: Session, category_id: int) -> Optional[Faq_Category]:
        """Get FAQ category by ID"""
        try:
            category = db.query(Faq_Category).filter(Faq_Category.id == category_id).first()
            return category
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while fetching category: {str(e)}"
            )
    
    @staticmethod
    def get_faq_title(db: Session)-> List[Faq_Category]:
        """Get all faq title"""
        return db.query(Faq_Category).order_by(Faq_Category.created_at.desc()).all()
    
    @staticmethod
    def create_faq_title(db: Session, faq_title:str) -> Faq_Category:
        """Post a faq title"""
        # Checks if the same title already exist in our database or not
        existing_faq_title = db.query(Faq_Category).filter(Faq_Category.title == faq_title).first()
        if existing_faq_title:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title already preasent, new title must be different from old one."
            )
        title = Faq_Category(faq_title)
        db.add(title)
        db.commit()
        db.refresh(title)
        return title
    
    @staticmethod
    def update_category(db: Session, category_id: int, category_data: Faq_Category) -> Optional[Faq_Category]:
        """Update an existing FAQ category"""
        try:
            db_category = Faq_Category.get_category_by_id(db, category_id)
            if not db_category:
                return None
            
            db_category.title = category_data.title
            db.commit()
            db.refresh(db_category)
            return db_category
        except SQLAlchemyError:
            db.rollback()
            raise

    


