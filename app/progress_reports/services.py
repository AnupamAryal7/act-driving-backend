
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status
from typing import List, Optional

from app.progress_reports.models import ProgressReport
from app.progress_reports.schemas import ProgressReportCreate, ProgressReportUpdate

# class ProgressReportService:

class ProgressReportService:
    # Get Operations
    @staticmethod
    def get_report_by_id(db:Session, report_id:int) -> ProgressReport:
        """Fet a single progress report by ID"""
        report = db.query(ProgressReport).filter(ProgressReport.id == report_id).first()
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Progress Report not Found"
            )
        return report
    
    @staticmethod
    def get_all_reports(db:Session, skip:int = 0, limit:int = 100, user_id:Optional[int] = None, course_id: Optional[int]= None) -> List[ProgressReport]:
        """Get all progress reports with optional filtering"""
        query = db.query(ProgressReport)

        if user_id is not None:
            query = query.filter(ProgressReport.user_id == user_id)

        if course_id is not None:
            query = query.filter(ProgressReport.course_id == course_id)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_user_progress(db: Session, user_id: int, course_id: int) -> ProgressReport:
        """Get a user's progress for a specific course"""
        report = db.query(ProgressReport).filter(
            and_(
                ProgressReport.user_id == user_id,
                ProgressReport.course_id == course_id
            )
        ).first()

        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Progress report for this user not found"
            )

        return report

    @staticmethod
    def create_report(db: Session, report_data: ProgressReportCreate) -> ProgressReport:
        """Create a new progress report"""
        existing_report = db.query(ProgressReport).filter(
            and_(
                ProgressReport.user_id == report_data.user_id,
                ProgressReport.course_id == report_data.course_id

            )
        ).first()
        if existing_report:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Progress report for this user already exist"
            )
        
        db_report = ProgressReport(
            user_id = report_data.user_id,
            course_id = report_data.course_id,
            progress_percentage = report_data.progress_percentage,
            status = report_data.status,
            feedback = report_data.feedback,
            remarks = report_data.remarks
        )

        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        return db_report

    
    @staticmethod
    def update_report(db: Session, report_id: int, report_data: ProgressReportUpdate) -> ProgressReport:
        """Update progress report"""
        report = ProgressReportService.get_report_by_id(db, report_id)
        update_data = report_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(report, field, value)

        db.commit()
        db.refresh(report)

        return report
    
    @staticmethod
    def update_progress_percentage(db: Session, report_id: int, percentage: float) -> ProgressReport:
        """Update only progress percentage for progress status"""
        if not 0 <= percentage <=100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Progress percentage must be in between 0 to 100 percentage"
            )
        
        report = ProgressReportService.get_report_by_id(db, report_id)
        report.progress_percentage = percentage

        #Auto update status based on percentage

        if percentage == 0:
            report.status = "not_started"
        
        elif percentage < 100:
            report.status = "in_progress"

        else:
            report.status = "completed"
        
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def delete_report(db: Session, report_id: int) -> None:
        """Delete a progress report"""
        report = ProgressReportService.get_report_by_id(db, report_id)
        db.delete(report)
        db.commit()

    @staticmethod
    def delete_user_reports(db: Session, user_id: int) -> None:
        """Delete all progress reports for a user"""
        db.query(ProgressReport).filter(ProgressReport.user_id == user_id).delete()
        db.commit()

# Utility function
def get_progress_report_service():
    return ProgressReportService


