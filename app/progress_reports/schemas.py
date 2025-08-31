
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProgressReportBase(BaseModel):
    user_id: int = Field(..., description="Id of user")
    course_id: int = Field(..., description="id of course")
    progress_percentage: float = Field(0.0, ge=0.0, le=100.0, description="Progress Percentage (0.0 to 100.0)")
    status: str = Field("not started", description="Progress status")
    feedback: Optional[str] = Field(None, description="Instructio feedback")
    remarks: Optional[str] = Field(None, max_length=80, description="Short Remarks")



# schemas for creating new records
class ProgressReportCreate(ProgressReportBase):
    pass


# Update schema for updating existing records(all fields optional)
class ProgressReportUpdate(BaseModel):
    progress_percentage: Optional[float] = Field(0.0, ge=0.0, le=100.0, description="Progress Percentage (0.0 to 100.0)")
    status: Optional[str] = Field("not started", description="Progress status")
    feedback: Optional[str] = Field(None, description="Instructio feedback")
    remarks: Optional[str] = Field(None, max_length=80, description="Short Remarks")


# Response schema
class ProgressReportInDBBase(ProgressReportBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProgressReport(ProgressReportInDBBase):
    pass


class ProgressReportInDB(ProgressReportInDBBase):
    pass
