from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.faq_categories.schemas import Faq_Category_Create, Faq_Category_Update, Faq_Category
from app.faq_categories.services import Faq_Category_Service

# add router
router = APIRouter(
    prefix="/api/v1/faq-categories",
    tags=["FAQ Categories"]
)

@router.get("/", response_model=List[Faq_Category])
def get_all_categories(db: Session = Depends(get_db)):
    """Get all FAQ categories"""
    try:
        categories = Faq_Category_Service.get_faq_title(db)
        return categories
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching FAQ categories: {str(e)}"
        )

@router.post("/", response_model=Faq_Category, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: Faq_Category_Create,
    db: Session = Depends(get_db)
):
    """Create a new FAQ category"""
    try:
        category = Faq_Category_Service.create_faq_title(db, category_data)
        return category
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating FAQ category: {str(e)}"
        )


@router.put("/{category_id}", response_model=Faq_Category)
def update_category(
    category_id: int,
    category_data: Faq_Category_Update,
    db: Session = Depends(get_db)
):
    """Update an existing FAQ category"""
    try:
        updated_category = Faq_Category_Service.update_category(db, category_id, category_data)
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
        success = Faq_Category_Service.delete_faq_category(db, category_id)
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