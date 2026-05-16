from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from datetime import datetime
from database import Base
import secrets
import string

def generate_license_key(length=16):
    """Generate a random license key like: X7K9-P4M2-V8N1-QW3R"""
    chars = string.ascii_uppercase + string.digits
    key = ''.join(secrets.choice(chars) for _ in range(length))
    # Format with dashes every 4 characters
    return '-'.join(key[i:i+4] for i in range(0, len(key), 4))

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, nullable=False, index=True)

    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, default=1)
    total_amount = Column(Numeric(10, 2), nullable=False)

    status = Column(String, default="pending")
    license_key = Column(String, unique=True, nullable=True)   # ← New
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
