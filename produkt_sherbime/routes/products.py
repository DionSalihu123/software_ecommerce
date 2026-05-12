from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from schemas import ProductCreate, ProductResponse
import crud

router = APIRouter()


# -----------------------------
# DATABASE SESSION
# -----------------------------
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# -----------------------------
# ROUTES
# -----------------------------
@router.post(
    "/products",
    response_model=ProductResponse
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return crud.create_product(db, product)


@router.get(
    "/products",
    response_model=List[ProductResponse]
)
def get_products(
    db: Session = Depends(get_db)
):
    return crud.get_products(db)


@router.get(
    "/products/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = crud.get_product_by_id(
        db,
        product_id
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product
