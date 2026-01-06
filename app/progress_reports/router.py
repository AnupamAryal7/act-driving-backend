from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional, List
import httpx

from app.database import get_db
from app.progress_reports.services import ProgressReportService
from app.progress_reports.schemas import (ProgressReport, ProgressReportCreate, ProgressReportUpdate)
from app.notifications.schemas import ProgressNotificationData

router = APIRouter(
    prefix="/progress-reports",
    tags=["progress-reports"]
)

# Background task function for progress report notifications
async def send_progress_notification(progress_data: ProgressNotificationData):
    """
    Send notification to student about progress report update
    This runs in the background
    """
    try:
        # Call our own notification endpoint
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://localhost:8000/api/v1/notifications/progress-report-updated",
                json=progress_data.dict()
            )
            if response.status_code != 200:
                print(f"Failed to send notification: {response.status_code}")
    except Exception as e:
        print(f"Error sending progress notification: {str(e)}")

@router.get("/", response_model=List[ProgressReport])
def get_all_progress_reports(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, le=500, description="Number of records to return"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    class_id: Optional[int] = Query(None, description="Filter by class ID"),
    db: Session = Depends(get_db)
):
    """Get all progress reports"""
    try:
        reports = ProgressReportService.get_all_reports(
            db=db, skip=skip, limit=limit, user_id=user_id, class_id=class_id
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
        report = ProgressReportService.get_report_by_id(db=db, report_id=report_id)
        return report
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching progress report: {str(e)}"
        )

@router.get("/user/{user_id}/class/{class_id}", response_model=ProgressReport)
def get_user_class_progress(
    user_id: int,
    class_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a user's progress report for a specific class session.
    """
    try:
        report = ProgressReportService.get_user_progress(
            db=db, user_id=user_id, class_id=class_id
        )
        return report
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user progress: {str(e)}"
        )

# CREATE endpoint with notification
@router.post("/", response_model=ProgressReport, status_code=status.HTTP_201_CREATED)
def create_progress_report(
    report_data: ProgressReportCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create a new progress report and notify student.
    """
    try:
        report = ProgressReportService.create_report(db=db, report_data=report_data)

        # Add background task for notification
        notification_data = ProgressNotificationData(
            user_id=report.user_id,
            progress_report_id=report.id,
            progress_percentage=report.progress_percentage,
            status=report.status
        )
        background_tasks.add_task(send_progress_notification, notification_data)

        return report
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating progress report: {str(e)}"
        )

# UPDATE endpoint with notification
@router.put("/{report_id}", response_model=ProgressReport)
def update_progress_report(
    report_id: int,
    report_data: ProgressReportUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Update a progress report and notify student.
    """
    try:
        report = ProgressReportService.update_report(
            db=db, report_id=report_id, report_data=report_data
        )

        # Add background task for notification
        notification_data = ProgressNotificationData(
            user_id=report.user_id,
            progress_report_id=report.id,
            progress_percentage=report.progress_percentage,
            status=report.status
        )
        background_tasks.add_task(send_progress_notification, notification_data)

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
    background_tasks: BackgroundTasks,
    report_id: int,
    percentage: float = Query(..., ge=0.0, le=100.0, description="Progress percentage (0.0 to 100.0)"),
    db: Session = Depends(get_db)
):
    """
    Update only the progress percentage of a report (automatically updates status) and notify student.
    """
    try:
        report = ProgressReportService.update_progress_percentage(
            db=db, report_id=report_id, percentage=percentage
        )

        # Add background task for notification
        notification_data = ProgressNotificationData(
            user_id=report.user_id,
            progress_report_id=report.id,
            progress_percentage=report.progress_percentage,
            status=report.status
        )
        background_tasks.add_task(send_progress_notification, notification_data)

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
        ProgressReportService.delete_user_reports(db=db, user_id=user_id)
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user progress reports: {str(e)}"
        )