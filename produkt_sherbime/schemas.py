from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    category: str
    version: Optional[str] = None
    license_type: str = "lifetime"

class ProductResponse(BaseModel):
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

    class Config:
        from_attributes = True
