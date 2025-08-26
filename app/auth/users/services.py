# from sqlalchemy.orm import Session
# from fastapi import HTTPException, status
# from typing import List, Optional

# from app.models import User
# from app.schemas import UserCreate, UserUpdate
from sqlalchemy import Text
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.auth.users.models import User
from app.auth.users.schemas import UserCreate


class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id:int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user not found"
            )
        return user
    @staticmethod
    def get_user_by_email(db: Session, email:str) -> User:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    @staticmethod
    def get_all_user(db:Session, skip: int=0, limit: int = 100, role: Optional[str]= None ) -> List[User]:
        query = db.query(User)

        if role:
            query = query.filter(User.role == role)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create_user(db: Session, user_data = UserCreate) -> User:
        #check if email already exist or not
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_NOT_FOUND,
                detail="User already exist, can't create new user using same email"
            )
        
        db_user = User(
            email = user_data.email,
            password = user_data.password,
            role = user_data.role
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def delete_user(db:Session, user_id: int) -> None:
        user = UserService.get_user_by_id(db, user_id)
        db.delete(user)
        db.commit()
        