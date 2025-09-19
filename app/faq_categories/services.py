from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.faq_categories.schemas import Faq_Category


class Faq_Category_Service:

    
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
    
    

