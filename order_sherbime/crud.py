from sqlalchemy.orm import Session
from fastapi import HTTPException
import httpx
import logging
from models import Order
from schemas import OrderCreate
from rabbitmq import publish_order_created
from decimal import Decimal

USER_SERVICE_URL = "http://user-service:8000"
PRODUCT_SERVICE_URL = "http://product-service:8000"

logging.basicConfig(level=logging.INFO)

def validate_user(user_id: int) -> dict:
    try:
        response = httpx.get(f"{USER_SERVICE_URL}/users/{user_id}", timeout=5.0)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=404, detail="User not found")
    except httpx.RequestError as e:
        logging.error(f"User service error: {e}")
        raise HTTPException(status_code=503, detail="User service unavailable")

def get_product_details(product_id: int) -> dict:
    try:
        response = httpx.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}", timeout=5.0)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=404, detail="Product not found")
    except httpx.RequestError as e:
        logging.error(f"Product service error: {e}")
        raise HTTPException(status_code=503, detail="Product service unavailable")

def create_order(db: Session, order: OrderCreate):
    # Validate user and product + get real data
    user = validate_user(order.user_id)
    product = get_product_details(order.product_id)

    # Calculate total
    price = Decimal(str(product["price"]))
    total_amount = price * order.quantity

    # Create order
    new_order = Order(
        user_id=order.user_id,
        product_id=order.product_id,
        price=price,
        quantity=order.quantity,
        total_amount=total_amount,
        status="pending"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Publish event
    publish_order_created({
        "order_id": new_order.id,
        "user_id": new_order.user_id,
        "product_id": new_order.product_id,
        "price": float(new_order.price),
        "total_amount": float(new_order.total_amount),
        "status": new_order.status,
        "quantity": new_order.quantity
    })

    return new_order

def get_orders(db: Session):
    return db.query(Order).all()
