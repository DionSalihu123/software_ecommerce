from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import OrderCreate, OrderResponse
import crud
from auth import get_current_user   # ← New import

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)   # ← Protected
):
    return crud.create_order(db, order, current_user_id)

@router.get("/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)
