from sqlalchemy.orm import Session

from models import Order
from schemas import OrderCreate


def create_order(
    db: Session,
    order: OrderCreate
):
    new_order = Order(
        user_id=order.user_id,
        product_id=order.product_id
    )

    db.add(new_order)

    db.commit()

    db.refresh(new_order)

    return new_order


def get_orders(db: Session):
    return db.query(Order).all()
