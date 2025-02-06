from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from app.models.users import User
from app.schemas.users import UserCreate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate, hashed_password: str):
    username = db.query(User).filter(User.username == user.username).first()
    if username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    db_user_by_email = db.query(User).filter(User.email == user.email).first()
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already taken"
        )

    db_user = User(
        username=user.username, email=user.email, password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "messages": "Success",
            "data": db_user.__dict__
        },
    )


def get_users(db: Session):
    return db.query(User).all()


def update_user(db: Session, user_id: int, updates: dict):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in updates.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
