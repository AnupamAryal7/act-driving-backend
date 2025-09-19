from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Faq_Category_Base(BaseModel):
        # id, title, creatd_at, updated_at
    title: str = Field(..., max_length=100, description="title of catgory")


class Faq_Category_Create(Faq_Category_Base):
    pass

class Faq_Category_Update(BaseModel):
    title: Optional[str] = Field(None, description="update title")

class Faq_Category_InDBBase(Faq_Category_Base):
    id: int
    created_at: datetime
    updated_at: datetime = None

    class Config:
        from_attributes: True

class Faq_Category(Faq_Category_InDBBase):
    pass

class Faq_Category_InDB(Faq_Category_InDBBase):
    pass 
