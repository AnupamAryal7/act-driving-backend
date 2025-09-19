from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.faqs.schemas import FAQ, FAQCreate, FAQUpdate
from app.faqs.services import FAQService

# add router
router = APIRouter(
    prefix="/faqs",
    tags=["FAQs"]
)

@router.get("/", response_model=List[FAQ])
def get_all_faqs(
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    db: Session = Depends(get_db)
):
    """Get all FAQs, optionally filtered by category"""
    try:
        return FAQService.get_all_faqs(db, category_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching FAQs: {str(e)}"
        )

@router.post("/", response_model=FAQ, status_code=status.HTTP_201_CREATED)
def create_faq(
    faq_data: FAQCreate,
    db: Session = Depends(get_db)
):
    """Create a new FAQ"""
    try:
        return FAQService.create_faq(db, faq_data)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating FAQ: {str(e)}"
        )

@router.get("/{faq_id}", response_model=FAQ)
def get_faq_by_id(
    faq_id: int,
    db: Session = Depends(get_db)
):
    """Get FAQ by ID"""
    try:
        faq = FAQService.get_faq_by_id(db, faq_id)
        if not faq:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"FAQ with ID {faq_id} not found"
            )
        return faq
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching FAQ: {str(e)}"
        )

@router.put("/{faq_id}", response_model=FAQ)
def update_faq(
    faq_id: int,
    faq_data: FAQUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing FAQ"""
    try:
        return FAQService.update_faq(db, faq_id, faq_data)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating FAQ: {str(e)}"
        )

@router.delete("/{faq_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faq(
    faq_id: int,
    db: Session = Depends(get_db)
):
    """Delete a FAQ"""
    try:
        FAQService.delete_faq(db, faq_id)
        return None
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting FAQ: {str(e)}"
        )