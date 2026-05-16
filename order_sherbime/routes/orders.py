from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import OrderCreate, OrderResponse, OrderStatusUpdate, PaymentRequest
import crud
from auth import get_current_user

router = APIRouter(tags=["Orders"])

@router.post("/orders/", response_model=OrderResponse, status_code=201)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    return crud.create_order(db, order, current_user_id)

@router.post("/orders/{order_id}/pay", response_model=OrderResponse)
def pay_order(
    order_id: int,
    payment: PaymentRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    return crud.pay_order(db, order_id, current_user_id, payment.payment_method)

@router.post("/orders/{order_id}/complete", response_model=OrderResponse)
def complete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    return crud.complete_order(db, order_id, current_user_id)

@router.get("/orders/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)

@router.get("/me/orders", response_model=List[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    return crud.get_orders_for_user(db, current_user_id)

@router.patch("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    return crud.update_order_status(db, order_id, status_update.status, current_user_id)
