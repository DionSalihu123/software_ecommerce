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

class ProductInfo(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: Decimal
    category: str
    version: Optional[str]
    license_type: str
    is_active: bool
    stock: int
    created_at: datetime
    updated_at: Optional[datetime]

class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    product: Optional[ProductInfo] = None
    price: Decimal
    quantity: int
    total_amount: Decimal
    status: str
    payment_status: str
    license_key: Optional[str] = None
    ordered_at: datetime
    paid_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
