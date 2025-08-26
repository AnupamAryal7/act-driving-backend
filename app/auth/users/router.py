
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.auth.users.schemas import UserCreate, UserResponse
from app.auth.users.services import UserService

# add router
router = APIRouter(
    tags=["users"]
)

@router.post("/",response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    #create a user
    try:
        return UserService.create_user(db, user)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


@router.get("/", response_model=List[UserResponse])
def get_all_users(skip:int = 0, limit:int = 100, role: Optional[str] = None, db: Session = Depends(get_db)):
    #get all user with optional filtering by role
    try:
        return UserService.get_all_user(db,skip,limit,role)
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users: {str(e)}"
        )


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id:int, db:Session = Depends(get_db)):
    #get user by id
    try:
        return UserService.get_user_by_id(db,user_id)
    except HTTPException as he:
        raise he
    except HTTPException as e:
        raise HTTPException (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error fetching user by id: {str(e)}"
        )


@router.get("/email/{email}", response_model=UserResponse)
def get_user_by_email(email:str, db:Session = Depends(get_db)):
    #get user by email
    try:
        user = UserService.get_user_by_email(db,email)
        if user:
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"no user found"
            )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error fetching data, error: {str(e)}"
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # delete user by id 
    try:
        user = UserService.get_user_by_id(db, user_id)
        db.delete(user)
        db.commit()
        return None
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )
