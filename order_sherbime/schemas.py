from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: int
    product_id: int


class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    status: str

    class Config:
        from_attributes = True
