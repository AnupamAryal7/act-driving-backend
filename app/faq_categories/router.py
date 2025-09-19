from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import FAQCategory, FAQCategoryCreate, FAQCategoryUpdate
from services import FAQCategoryService

# add router
router = APIRouter(
    prefix="/api/v1/faq-categories",
    tags=["FAQ Categories"]
)

@router.get("/", response_model=List[FAQCategory])
def get_all_categories(db: Session = Depends(get_db)):
    """Get all FAQ categories"""
    try:
        categories = FAQCategoryService.get_all_categories(db)
        return categories
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching FAQ categories: {str(e)}"
        )

@router.post("/", response_model=FAQCategory, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: FAQCategoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new FAQ category"""
    try:
        category = FAQCategoryService.create_category(db, category_data)
        return category
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating FAQ category: {str(e)}"
        )


@router.put("/{category_id}", response_model=FAQCategory)
def update_category(
    category_id: int,
    category_data: FAQCategoryUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing FAQ category"""
    try:
        updated_category = FAQCategoryService.update_category(db, category_id, category_data)
        if not updated_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"FAQ category with ID {category_id} not found"
            )
        return updated_category
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating FAQ category: {str(e)}"
        )

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """Delete a FAQ category"""
    try:
        success = FAQCategoryService.delete_category(db, category_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"FAQ category with ID {category_id} not found"
            )
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting FAQ category: {str(e)}"
        )