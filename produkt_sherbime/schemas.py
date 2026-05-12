from pydantic import BaseModel
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    stock: int
    created_at: datetime

    class Config:
        from_attributes = True
