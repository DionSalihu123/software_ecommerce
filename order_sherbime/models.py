from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean
from datetime import datetime
from database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, nullable=False, index=True)

    # Fetch and store price at order time (important for digital goods)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, default=1)
    total_amount = Column(Numeric(10, 2), nullable=False)

    status = Column(String, default="pending")  # pending, paid, completed, failed, cancelled
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
