from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import UserCreate, UserResponse
import crud

router = APIRouter()


# -----------------------------
# CREATE USER
# -----------------------------
@router.post("/users", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(db, user)


# -----------------------------
# GET ALL USERS
# -----------------------------
@router.get("/users", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):
    return crud.get_users(db)


# -----------------------------
# GET USER BY ID  (IMPORTANT FOR ORDER SERVICE)
# -----------------------------
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
