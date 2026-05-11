from fastapi import FastAPI
from pydantic import BaseModel

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

import time


# prite data bazen
time.sleep(10)


# DATABASE URL
DATABASE_URL = "postgresql://postgres:password@postgres-db:5432/ecommerce"


# SQLAlchemy setup
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# DATABASE MODEL
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)


# CREATE TABLES
Base.metadata.create_all(bind=engine)


# FASTAPI APP
app = FastAPI()


# REQUEST MODEL
class User(BaseModel):
    username: str
    email: str


# ROUTES
@app.get("/")
def home():
    return {"message": "User Service Running"}


@app.post("/users")
def create_user(user: User):

    db = SessionLocal()

    new_user = UserDB(
        username=user.username,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.close()

    return {
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    }


@app.get("/users")
def get_users():

    db = SessionLocal()

    users = db.query(UserDB).all()

    db.close()

    return users
