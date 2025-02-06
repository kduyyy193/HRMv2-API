from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.data_access.db import SessionLocal
from app.services.auth import get_admin_user
from app.services.users import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from app.schemas.users import UserCreate, UserResponse
from app.repositories.users import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    get_users
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token = create_access_token(data={
        "sub": user.email,
        "role": user.role
    })
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    username = get_user_by_username(db, user.username)
    if username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    db_user_by_email = get_user_by_email(db, user.email)
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already taken"
        )
    hashed_password = get_password_hash(user.password)
    new_user = create_user(db, user, hashed_password)
    return new_user


@router.get("/users", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int, db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user)
):
    return delete_user(user_id, db)
