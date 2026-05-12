from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate


def create_user(db: Session, user: UserCreate):

    new_user = User(
        username=user.username,
        email=user.email
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


def get_users(db: Session):

    return db.query(User).all()
