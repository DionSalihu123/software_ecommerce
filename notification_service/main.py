from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Notification Service Running"}

@app.post("/notify")
def notify(message: str):
    print(f"NOTIFICATION SENT: {message}")
    return {"status": "sent", "message": message}
