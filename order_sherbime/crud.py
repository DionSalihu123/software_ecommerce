from sqlalchemy.orm import Session
from fastapi import HTTPException
import httpx
import logging

from models import Order
from schemas import OrderCreate
from rabbitmq import publish_order_created


USER_SERVICE_URL = "http://user-service:8000"
PRODUCT_SERVICE_URL = "http://product-service:8000"


# -----------------------------
# USER VALIDATION
# -----------------------------
def validate_user(user_id: int) -> bool:
    try:
        response = httpx.get(
            f"{USER_SERVICE_URL}/users/{user_id}",
            timeout=3.0
        )

        return response.status_code == 200

    except httpx.RequestError as e:
        logging.error(f"User service error: {e}")
        return False


# -----------------------------
# PRODUCT VALIDATION
# -----------------------------
def validate_product(product_id: int) -> bool:
    try:
        response = httpx.get(
            f"{PRODUCT_SERVICE_URL}/products/{product_id}",
            timeout=3.0
        )

        return response.status_code == 200

    except httpx.RequestError as e:
        logging.error(f"Product service error: {e}")
        return False


# -----------------------------
# CREATE ORDER
# -----------------------------
def create_order(db: Session, order: OrderCreate):

    # validate user
    if not validate_user(order.user_id):
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # validate product
    if not validate_product(order.product_id):
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # create order
    new_order = Order(
        user_id=order.user_id,
        product_id=order.product_id
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # publish event
    publish_order_created({
        "order_id": new_order.id,
        "user_id": new_order.user_id,
        "product_id": new_order.product_id,
        "status": new_order.status
    })

    return new_order


# -----------------------------
# GET ORDERS
# -----------------------------
def get_orders(db: Session):
    return db.query(Order).all()
