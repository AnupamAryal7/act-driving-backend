from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.reviews.schemas import ReviewResponse, ReviewCreate, ReviewUpdate
from app.reviews import services

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.get("/", response_model=List[ReviewResponse])
def get_all_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all reviews with pagination"""
    reviews = services.get_all_reviews(db, skip=skip, limit=limit)
    return reviews

@router.get("/approved", response_model=List[ReviewResponse])
def get_approved_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all approved reviews with pagination"""
    reviews = services.get_approved_reviews(db, skip=skip, limit=limit)
    return reviews

@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    """Get a specific review by ID"""
    review = services.get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.get("/course/{course_title}", response_model=List[ReviewResponse])
def get_reviews_by_course(
    course_title: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get reviews for a specific course"""
    reviews = services.get_reviews_by_course(db, course_title, skip=skip, limit=limit)
    return reviews

@router.post("/", response_model=ReviewResponse, status_code=201)
def add_review(review: ReviewCreate, db: Session = Depends(get_db)):
    """Create a new review"""
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    return services.add_review(db, review)

@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(
    review_id: int, 
    review_update: ReviewUpdate, 
    db: Session = Depends(get_db)
):
    """Update an existing review"""
    if review_update.rating is not None and (review_update.rating < 1 or review_update.rating > 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    updated_review = services.update_review(db, review_id, review_update)
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review

@router.delete("/{review_id}", status_code=204)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    """Delete a review"""
    success = services.delete_review(db, review_id)
    if not success:
        raise HTTPException(status_code=404, detail="Review not found")