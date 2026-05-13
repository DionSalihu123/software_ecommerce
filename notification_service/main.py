from fastapi import FastAPI
import threading
import logging
from consumer import consume_messages

app = FastAPI(title="Notification Service")

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
