
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database import get_db
from app.progress_reports.services import ProgressReportService
from app.progress_reports.schemas import (ProgressReport, ProgressReportCreate, ProgressReportUpdate)

router = APIRouter(
    prefix="/progress-reports",
    tags=["progress-reports"]
)



@router.get("/", response_model=List[ProgressReport])
def get_all_progress_reports(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, le=500, description="Number of records to return"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    course_id: Optional[int] = Query(None, description="Filter by course ID"),
    db: Session = Depends(get_db)
):
    """GEt all progress reports"""
    try:
        # service = ProgressReportService()
        reports = ProgressReportService.get_all_reports(
            db=db,
            skip=skip,
            limit=limit,
            user_id=user_id,
            course_id=course_id
        )
        return reports
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Report not found!!!"
        )


    """
    Get all progress reports with optional filtering by user_id and/or course_id.
    """
    try:
        service = ProgressReportService()
        reports = service.get_all_reports(
            db=db, 
            skip=skip, 
            limit=limit, 
            user_id=user_id, 
            course_id=course_id
        )
        return reports
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching progress reports: {str(e)}"
        )

@router.get("/{report_id}", response_model=ProgressReport)
def get_progress_report_by_id(
    report_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific progress report by ID.
    """
    try:
        # service = ProgressReportService()
        report = ProgressReportService.get_report_by_id(db=db, report_id=report_id)
        return report
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching progress report: {str(e)}"
        )

@router.get("/user/{user_id}/course/{course_id}", response_model=ProgressReport)
def get_user_course_progress(
    user_id: int,
    course_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a user's progress report for a specific course.
    """
    try:
        # service = ProgressReportService()
        report = ProgressReportService.get_user_progress(
            db=db, 
            user_id=user_id, 
            course_id=course_id
        )
        return report
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user progress: {str(e)}"
        )

@router.post("/", response_model=ProgressReport, status_code=status.HTTP_201_CREATED)
def create_progress_report(
    report_data: ProgressReportCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new progress report.
    """
    try:
        # service = ProgressReportService()
        report = ProgressReportService.create_report(db=db, report_data=report_data)
        return report
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating progress report: {str(e)}"
        )

@router.put("/{report_id}", response_model=ProgressReport)
def update_progress_report(
    report_id: int,
    report_data: ProgressReportUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a progress report.
    """
    try:
        # service = ProgressReportService()
        report = ProgressReportService.update_report(
            db=db, 
            report_id=report_id, 
            report_data=report_data
        )
        return report
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating progress report: {str(e)}"
        )

@router.patch("/{report_id}/progress", response_model=ProgressReport)
def update_progress_percentage(
    report_id: int,
    percentage: float = Query(..., ge=0.0, le=100.0, description="Progress percentage (0.0 to 100.0)"),
    db: Session = Depends(get_db)
):
    """
    Update only the progress percentage of a report (automatically updates status).
    """
    try:
        # service = ProgressReportService()
        report = ProgressReportService.update_progress_percentage(
            db=db, 
            report_id=report_id, 
            percentage=percentage
        )
        return report
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating progress percentage: {str(e)}"
        )

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_progress_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a specific progress report.
    """
    try:
        # service = ProgressReportService()
        ProgressReportService.delete_report(db=db, report_id=report_id)
        return None
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting progress report: {str(e)}"
        )

@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_progress_reports(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete all progress reports for a specific user.
    """
    try:
        # service = ProgressReportService()
        ProgressReportService.delete_user_reports(db=db, user_id=user_id)
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user progress reports: {str(e)}"
        )