from fastapi import FastAPI

app = FastAPI()

users = []

@app.get("/")
def home():
    return {"message": "User Service Running"}

@app.post("/register")
def register(username: str, password: str):
    user = {
        "username": username,
        "password": password
    }

    users.append(user)

    return {
        "message": "User registered successfully",
        "user": username
    }

@app.get("/users")
def get_users():
    return users
