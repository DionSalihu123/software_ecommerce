from fastapi import FastAPI
import logging

from database import engine, Base
from routes.orders import router as orders_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

logging.basicConfig(level=logging.INFO)

app.include_router(orders_router)


@app.get("/")
def home():
    return {"message": "Order Service Running"}
