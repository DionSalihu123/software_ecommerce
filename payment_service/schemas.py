from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class PaymentRequest(BaseModel):
    order_id: int
    amount: Decimal
    payment_method: str = "card"
    currency: str = "USD"
    metadata: Optional[dict] = None

class PaymentResponse(BaseModel):
    order_id: int
    transaction_id: str
    status: str
    amount: Decimal
    currency: str
    payment_method: str
    paid_at: str
