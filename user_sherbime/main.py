import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes.users import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")

origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

app.include_router(user_router)

@app.get("/")
def home():
    return {"message": "User Service Running ✅"}

@app.get("/health")
def health():
    return {"status": "healthy"}
