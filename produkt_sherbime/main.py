from fastapi import FastAPI

from database import engine, Base
from routes.products import router as products_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(products_router)
