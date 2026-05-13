from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: Optional[int] = 1   # Made optional with default

class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    price: Decimal
    quantity: int
    total_amount: Decimal
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
