from sqlalchemy.orm import Session
from fastapi import HTTPException
import httpx
import logging
from models import Order, generate_license_key
from schemas import OrderCreate
from rabbitmq import publish_order_created
from decimal import Decimal

PRODUCT_SERVICE_URL = "http://product-service:8000"

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

    # Generate License Key for digital products
    license_key = generate_license_key()

    new_order = Order(
        user_id=user_id,
        product_id=order.product_id,
        price=price,
        quantity=order.quantity,
        total_amount=total_amount,
        status="pending",
        license_key=license_key
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Publish event with license key
    publish_order_created({
        "order_id": new_order.id,
        "user_id": new_order.user_id,
        "product_id": new_order.product_id,
        "price": float(new_order.price),
        "total_amount": float(new_order.total_amount),
        "status": new_order.status,
        "quantity": new_order.quantity,
        "license_key": new_order.license_key
    })

    return new_order

def get_orders(db: Session):
    return db.query(Order).all()
