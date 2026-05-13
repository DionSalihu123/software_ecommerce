from fastapi import FastAPI
import logging
from database import engine, Base
from routes.products import router as products_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Service")

logging.basicConfig(level=logging.INFO)

app.include_router(products_router)

@app.get("/")
def home():
    return {"message": "Product Service Running ✅"}
