from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime
from typing import List

DATABASE_URL = "postgresql://postgres:password@postgres-db:5432/ecommerce"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

app = FastAPI()


# -----------------------------
# DATABASE MODEL
# -----------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, nullable=False)

    email = Column(String, unique=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


# -----------------------------
# PYDANTIC SCHEMAS
# -----------------------------

class UserCreate(BaseModel):
    username: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# -----------------------------
# DATABASE SESSION
# -----------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# -----------------------------
# ROUTES
# -----------------------------

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        username=user.username,
        email=user.email
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


@app.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return users
