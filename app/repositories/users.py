from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.users import UserCreate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate, hashed_password: str):
    db_user = User(
        username=user.username, email=user.email, password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def count_users(db: Session):
    return db.query(User).count()


def update_user_by_id(db: Session, user_id: int, updates: dict):
    user = db.query(User).filter(User.id == user_id).one()
    if not user:
        return {"error": "User not found"}

    for key, value in updates.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
