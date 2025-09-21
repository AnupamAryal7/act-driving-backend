from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from sqlalchemy import or_

from app.auth.users.models import User
from app.auth.users.schemas import UserCreate, UserUpdate
from app.auth.utils.password import hash_password, verify_password

class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_phone(db: Session, phone_number: str) -> User:
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found with this phone number"
            )
        return user
    
    @staticmethod
    def search_users(db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).filter(
            or_(
                User.full_name.ilike(f"%{search_term}%"),
                User.email.ilike(f"%{search_term}%"),
                User.phone_number.ilike(f"%{search_term}%")
            )
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_all_user(db: Session, skip: int = 0, limit: int = 100, role: Optional[str] = None) -> List[User]:
        query = db.query(User)
        if role:
            query = query.filter(User.role == role)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists with this email"
            )
        
        # Check if phone number already exists (if provided)
        if user_data.phone_number:
            existing_phone_user = db.query(User).filter(User.phone_number == user_data.phone_number).first()
            if existing_phone_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User already exists with this phone number"
                )
        
        hashed_password = hash_password(user_data.password)
        
        db_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            phone_number=user_data.phone_number,
            password=hashed_password,
            role=user_data.role
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
        user = UserService.get_user_by_id(db, user_id)
        
        # Check if phone number already exists (if provided and changing)
        if user_data.phone_number and user_data.phone_number != user.phone_number:
            existing_phone_user = db.query(User).filter(
                User.phone_number == user_data.phone_number,
                User.id != user_id
            ).first()
            if existing_phone_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Another user already exists with this phone number"
                )
        
        # Update fields if provided
        if user_data.full_name is not None:
            user.full_name = user_data.full_name
        if user_data.phone_number is not None:
            user.phone_number = user_data.phone_number
        if user_data.role is not None:
            user.role = user_data.role
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> None:
        user = UserService.get_user_by_id(db, user_id)
        db.delete(user)
        db.commit()
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        user = UserService.get_user_by_email(db, email)
        
        # If no user found with this email
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # If user found but password doesn't match
        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        return user