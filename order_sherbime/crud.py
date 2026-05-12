from sqlalchemy.orm import Session
from fastapi import HTTPException
from rabbitmq import publish_order_created
import httpx

from models import Order
from schemas import OrderCreate


USER_SERVICE_URL = "http://user-service:8000"
PRODUCT_SERVICE_URL = "http://product-service:8000"


def validate_user(user_id: int):

    response = httpx.get(
        f"{USER_SERVICE_URL}/users"
    )

    users = response.json()

    for user in users:
        if user["id"] == user_id:
            return True

    return False


def validate_product(product_id: int):

    response = httpx.get(
        f"{PRODUCT_SERVICE_URL}/products/{product_id}"
    )

    return response.status_code == 200


def create_order(
    db: Session,
    order: OrderCreate
):

    # -----------------------------
    # VALIDATE USER
    # -----------------------------
    if not validate_user(order.user_id):

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # -----------------------------
    # VALIDATE PRODUCT
    # -----------------------------
    if not validate_product(order.product_id):

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # -----------------------------
    # CREATE ORDER
    # -----------------------------
    new_order = Order(
        user_id=order.user_id,
        product_id=order.product_id
    )

    db.add(new_order)

    db.commit()

    db.refresh(new_order)

    publish_order_created({
    "order_id": new_order.id,
    "user_id": new_order.user_id,
    "product_id": new_order.product_id,
    "status": new_order.status
    })

    return new_order


def get_orders(db: Session):
    return db.query(Order).all()
