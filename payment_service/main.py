import os
import uuid
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import PaymentRequest, PaymentResponse

app = FastAPI(title="Payment Service")

origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Payment Service Running ✅"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/payments/", response_model=PaymentResponse)
def create_payment(payment: PaymentRequest):
    transaction_id = uuid.uuid4().hex.upper()
    return PaymentResponse(
        order_id=payment.order_id,
        transaction_id=transaction_id,
        status="success",
        amount=payment.amount,
        currency=payment.currency,
        payment_method=payment.payment_method,
        paid_at=datetime.utcnow().isoformat() + "Z"
    )
