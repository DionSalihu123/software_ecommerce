import secrets
import string
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from datetime import datetime
from database import Base


def generate_license_key(length: int = 24) -> str:
    allowed = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(allowed) for _ in range(length))


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, nullable=False, index=True)

    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, default=1)
    total_amount = Column(Numeric(10, 2), nullable=False)

    # Improved Status
    status = Column(String, default="pending")  # pending, paid, completed, failed, cancelled
    license_key = Column(String, unique=True, nullable=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
