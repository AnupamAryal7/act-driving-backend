from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status, UploadFile
from typing import Optional, List

from app.courses.models import Course
from app.courses.schemas import CourseCreate, CourseUpdate
from app.services.cloudinary_service import CloudinaryService


class CourseService:
    @staticmethod
    def get_course_by_id(db: Session, course_id: int) -> Course:
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="course not found"
            )
        return course
    
    @staticmethod
    def get_all_courses(db: Session, skip: int = 0, limit: int = 100, is_active: Optional[bool] = None) -> List[Course]:
        query = db.query(Course)

        if is_active is not None:
            query = query.filter(Course.is_active == is_active)

        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_active_courses(db: Session) -> List[Course]:
        return db.query(Course).filter(Course.is_active == True).all()
    
    @staticmethod
    def search_courses(
        db: Session,
        search_term: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Course]:
        search_pattern = f"%{search_term}%"
        return db.query(Course).filter(Course.course_title.ilike(search_pattern)).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_course(db: Session, course_data: CourseCreate) -> Course:
        db_course = Course(
            course_title=course_data.course_title,
            description=course_data.description,
            bullet_pt1=course_data.bullet_pt1,
            bullet_pt2=course_data.bullet_pt2,
            bullet_pt3=course_data.bullet_pt3,
            duration=course_data.duration,
            package_type=course_data.package_type,
            total_price=course_data.total_price,
            discounted_price=course_data.discounted_price,
            is_active=course_data.is_active,
            image_url=course_data.image_url,
            image_public_id=course_data.image_public_id
        )
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course
    
    @staticmethod
    def update_course(db: Session, course_id: int, course_data: CourseUpdate) -> Course:
        course = CourseService.get_course_by_id(db, course_id)

        update_data = course_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(course, field, value)
        
        db.commit()
        db.refresh(course)
        return course
    
    @staticmethod
    async def update_course_image(db: Session, course_id: int, image_file: UploadFile) -> Course:
        course = CourseService.get_course_by_id(db, course_id)
        
        # Delete old image if exists
        if course.image_public_id:
            CloudinaryService.delete_image(course.image_public_id)
        
        # Upload new image
        image_result = await CloudinaryService.upload_course_image(image_file, course_id)
        
        # Update course with new image info
        course.image_url = image_result["url"]
        course.image_public_id = image_result["public_id"]
        
        db.commit()
        db.refresh(course)
        return course
    
    @staticmethod
    def delete_course_image(db: Session, course_id: int) -> Course:
        course = CourseService.get_course_by_id(db, course_id)
        
        if course.image_public_id:
            CloudinaryService.delete_image(course.image_public_id)
            course.image_url = None
            course.image_public_id = None
            
            db.commit()
            db.refresh(course)
        
        return course
    
    @staticmethod
    def delete_course(db: Session, course_id: int) -> None:
        course = CourseService.get_course_by_id(db, course_id)
        course.is_active = False
        db.commit()
    
    @staticmethod
    def hard_delete_course(db: Session, course_id: int) -> None:
        course = CourseService.get_course_by_id(db, course_id)
        
        # Delete associated image from Cloudinary
        if course.image_public_id:
            CloudinaryService.delete_image(course.image_public_id)
        
        db.delete(course)
        db.commit()
    
    @staticmethod
    def restore_course_by_id(db: Session, course_id: int) -> Course:
        course = CourseService.get_course_by_id(db, course_id)
        course.is_active = True
        db.commit()
        db.refresh(course)
        return course
    
    @staticmethod
    def get_courses_by_price_range(
        db: Session,
        min_price: float,
        max_price: float,
        is_active: bool = True
    ) -> List[Course]:
        return db.query(Course).filter(
            Course.discounted_price >= min_price,
            Course.discounted_price <= max_price,
            Course.is_active == is_active
        ).all()
    
    @staticmethod
    def get_courses_by_package_type(
        db: Session, 
        package_type: str,
        is_active: bool = True
    ) -> List[Course]:
        return db.query(Course).filter(
            Course.package_type == package_type,
            Course.is_active == is_active
        ).all()