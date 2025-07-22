from sqlalchemy.orm import Session
from app.reviews.models import Review
from app.reviews.schemas import ReviewCreate, ReviewUpdate
from typing import List, Optional

def get_all_reviews(db: Session, skip: int = 0, limit: int = 100) -> List[Review]:
    return db.query(Review).offset(skip).limit(limit).all()

def get_review_by_id(db: Session, review_id: int) -> Optional[Review]:
    return db.query(Review).filter(Review.id == review_id).first()

def get_reviews_by_course(db: Session, course_title: str, skip: int = 0, limit: int = 100) -> List[Review]:
    return db.query(Review).filter(Review.course_title == course_title).offset(skip).limit(limit).all()

def get_approved_reviews(db: Session, skip: int = 0, limit: int = 100) -> List[Review]:
    return db.query(Review).filter(Review.is_approved == True).offset(skip).limit(limit).all()

def add_review(db: Session, review: ReviewCreate) -> Review:
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def update_review(db: Session, review_id: int, review_update: ReviewUpdate) -> Optional[Review]:
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review:
        update_data = review_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_review, field, value)
        db.commit()
        db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: int) -> bool:
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
        return True
    return False
