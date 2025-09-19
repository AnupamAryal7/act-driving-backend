from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FAQBase(BaseModel):
    category_id: int = Field(..., description="Linked FAQCategory ID")
    question: str = Field(..., max_length=500, description="The FAQ question")
    answer: str = Field(..., description="The FAQ answer")

class FAQCreate(FAQBase):
    pass

class FAQUpdate(BaseModel):
    category_id: Optional[int] = Field(None, description="Linked FAQCategory ID")
    question: Optional[str] = Field(None, max_length=500, description="The FAQ question")
    answer: Optional[str] = Field(None, description="The FAQ answer")

class FAQInDBBase(FAQBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class FAQ(FAQInDBBase):
    pass

class FAQWithCategory(FAQ):
    category_title: Optional[str] = None