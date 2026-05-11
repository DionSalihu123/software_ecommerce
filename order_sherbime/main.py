from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from models import Base, Order
from database import engine, SessionLocal

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/orders")
def create_order(user_id: int, product_id: int, db: Session = Depends(get_db)):
    order = Order(user_id=user_id, product_id=product_id)

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()
