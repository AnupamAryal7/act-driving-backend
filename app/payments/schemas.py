from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import enum

# Define Enum for Payment Status (matches database enum)
class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed" 
    REFUNDED = "refunded"

# Base schema - common fields
class PaymentBase(BaseModel):
    student_id: int = Field(..., description="ID of the student user")
    course_id: int = Field(..., description="ID of the course")
    amount: float = Field(..., gt=0, description="Payment amount (must be positive)")
    status: PaymentStatus = Field(PaymentStatus.PENDING, description="Payment status")
    payment_method: str = Field(..., description="Payment method used")
    transaction_id: Optional[str] = Field(None, description="Unique transaction ID from payment gateway")

# Create schema - for creating new payments
class PaymentCreate(PaymentBase):
    pass

# Update schema - for updating existing payments
class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = Field(None, description="Payment status")
    transaction_id: Optional[str] = Field(None, description="Unique transaction ID from payment gateway")

# Response schema - what gets returned from API
class PaymentInDBBase(PaymentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Enable ORM mode

class Payment(PaymentInDBBase):
    pass

class PaymentInDB(PaymentInDBBase):
    pass