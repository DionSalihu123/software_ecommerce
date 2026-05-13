from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Product
from schemas import ProductCreate
from datetime import datetime

def create_product(db: Session, product: ProductCreate):
    # Check if product with same name already exists
    if db.query(Product).filter(Product.name == product.name).first():
        raise HTTPException(status_code=400, detail="Product with this name already exists")

    new_product = Product(
        **product.model_dump(),
        stock=9999,           # Digital products usually unlimited
        is_active=True
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).filter(Product.is_active == True).offset(skip).limit(limit).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_product_by_id_or_404(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    if not product or not product.is_active:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
