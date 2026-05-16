from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional

class OrderCreate(BaseModel):
    product_id: int
    quantity: Optional[int] = 1

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

    class Config:
        from_attributes = True
