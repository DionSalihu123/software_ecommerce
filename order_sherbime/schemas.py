from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional

class OrderCreate(BaseModel):
    product_id: int
    quantity: Optional[int] = 1

class PaymentRequest(BaseModel):
    payment_method: Optional[str] = "card"
    transaction_id: Optional[str] = None

class OrderStatusUpdate(BaseModel):
    status: str  # pending, paid, completed, failed, cancelled

class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    price: Decimal
    quantity: int
    total_amount: Decimal
    status: str
    license_key: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
