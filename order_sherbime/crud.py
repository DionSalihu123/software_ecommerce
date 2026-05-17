from sqlalchemy.orm import Session
from fastapi import HTTPException
import httpx
import logging
from models import Order, generate_license_key
from schemas import OrderCreate
from rabbitmq import publish_order_created
from decimal import Decimal
from datetime import datetime
import os

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8000")
PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL", "http://payment-service:8000")


def get_product_details(product_id: int) -> dict:
    try:
        response = httpx.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}", timeout=5.0)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=404, detail="Product not found")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Product service unavailable")


def create_order(db: Session, order: OrderCreate, user_id: int):
    product = get_product_details(order.product_id)

    price = Decimal(str(product["price"]))
    total_amount = price * order.quantity

    new_order = Order(
        user_id=user_id,
        product_id=order.product_id,
        price=price,
        quantity=order.quantity,
        total_amount=total_amount,
        status="pending",
        payment_status="unpaid",
        license_key=None
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


def attach_product_details(order: Order):
    try:
        product = get_product_details(order.product_id)
        order.product = product
    except HTTPException:
        order.product = None
    return order


def get_orders(db: Session):
    orders = db.query(Order).all()
    return [attach_product_details(order) for order in orders]


def get_orders_for_user(db: Session, user_id: int):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return [attach_product_details(order) for order in orders]


def get_order_by_id(db: Session, order_id: int, user_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return attach_product_details(order)


def pay_order(db: Session, order_id: int, user_id: int, payment_method: str = "card"):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Only pending orders can be paid")

    payment_data = {
        "order_id": order.id,
        "amount": float(order.total_amount),
        "payment_method": payment_method,
        "currency": "USD",
    }

    try:
        response = httpx.post(f"{PAYMENT_SERVICE_URL}/payments/", json=payment_data, timeout=10.0)
        response.raise_for_status()
        payment_result = response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Payment service unavailable: {e}")
    except httpx.HTTPStatusError:
        order.status = "failed"
        order.payment_status = "failed"
        db.commit()
        db.refresh(order)
        raise HTTPException(status_code=response.status_code, detail="Payment failed")

    if payment_result.get("status") != "success":
        order.status = "failed"
        order.payment_status = "failed"
        db.commit()
        db.refresh(order)
        raise HTTPException(status_code=402, detail="Payment failed")

    order.status = "paid"
    order.payment_status = "paid"
    order.paid_at = datetime.utcnow()
    db.commit()
    db.refresh(order)

    return order


def complete_order(db: Session, order_id: int, user_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "paid" or order.payment_status != "paid":
        raise HTTPException(status_code=400, detail="Only paid orders can be completed")

    order.license_key = generate_license_key()
    order.status = "completed"
    order.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(order)

    publish_order_created({
        "order_id": order.id,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "price": float(order.price),
        "total_amount": float(order.total_amount),
        "status": order.status,
        "quantity": order.quantity,
        "license_key": order.license_key
    })

    return order


def update_order_status(db: Session, order_id: int, new_status: str, user_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    valid_transitions = {
        "pending": ["paid", "completed", "cancelled"],
        "paid": ["completed", "failed", "cancelled"],
        "completed": [],
        "failed": [],
        "cancelled": []
    }

    current_status = order.status
    if new_status == current_status:
        return order

    if current_status not in valid_transitions or new_status not in valid_transitions[current_status]:
        raise HTTPException(status_code=400, detail=f"Invalid status transition from {current_status} to {new_status}")

    if new_status == "failed":
        order.payment_status = "failed"
        order.failed_at = datetime.utcnow()
    elif new_status == "cancelled":
        order.payment_status = "cancelled"
        order.cancelled_at = datetime.utcnow()

    if new_status == "completed" and not order.license_key:
        order.license_key = generate_license_key()
    if new_status == "completed":
        order.completed_at = datetime.utcnow()

    order.status = new_status
    db.commit()
    db.refresh(order)

    if new_status == "completed":
        publish_order_created({
            "order_id": order.id,
            "user_id": order.user_id,
            "product_id": order.product_id,
            "status": order.status,
            "license_key": order.license_key
        })

    return order
