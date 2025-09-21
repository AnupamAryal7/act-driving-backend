from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.auth.users.schemas import UserCreate, UserResponse, UserLogin, UserUpdate
from app.auth.users.services import UserService

router = APIRouter(
    tags=["users"]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return UserService.create_user(db, user)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@router.get("/", response_model=List[UserResponse])
def get_all_users(
    skip: int = 0, 
    limit: int = 100, 
    role: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    try:
        return UserService.get_all_user(db, skip, limit, role)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users: {str(e)}"
        )

@router.get("/search/", response_model=List[UserResponse])  # New endpoint
def search_users(
    q: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    try:
        return UserService.search_users(db, q, skip, limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching users: {str(e)}"
        )

@router.get("/phone/{phone_number}", response_model=UserResponse)  # New endpoint
def get_user_by_phone(phone_number: str, db: Session = Depends(get_db)):
    try:
        return UserService.get_user_by_phone(db, phone_number)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user by phone: {str(e)}"
        )

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        return UserService.get_user_by_id(db, user_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user by id: {str(e)}"
        )

@router.get("/email/{email}", response_model=UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    try:
        return UserService.get_user_by_email(db, email)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user by email: {str(e)}"
        )

@router.put("/{user_id}", response_model=UserResponse)  # New endpoint
def update_user(
    user_id: int, 
    user_data: UserUpdate, 
    db: Session = Depends(get_db)
):
    try:
        return UserService.update_user(db, user_id, user_data)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        UserService.delete_user(db, user_id)
        return None
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )

@router.post("/login")
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    try:
        user = UserService.authenticate_user(db, login_data.email, login_data.password)
        return {
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "phone_number": user.phone_number,  # Added
                "role": user.role
            }
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )