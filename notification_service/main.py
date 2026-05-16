import os
import threading
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from consumer import consume_messages

app = FastAPI(title="Notification Service")

origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

@app.get("/")
def home():
    return {"message": "Notification Service Running ✅"}

@app.get("/health")
def health():
    return {"status": "healthy"}

def start_consumer():
    logging.info("🚀 Starting RabbitMQ consumer thread...")
    thread = threading.Thread(target=consume_messages, daemon=True)
    thread.start()

@app.on_event("startup")
def startup_event():
    start_consumer()
