from fastapi import FastAPI
import logging
from database import engine, Base
from routes.users import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")

logging.basicConfig(level=logging.INFO)

app.include_router(user_router)

@app.get("/")
def home():
    return {"message": "User Service Running ✅"}
