from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import UserCreate, UserResponse
import crud

router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    return crud.create_user(db, user)


@router.get("/users", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):

    return crud.get_users(db)
