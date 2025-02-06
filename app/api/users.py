from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.data_access.db import SessionLocal
from app.models.users import UserRole
from app.services.auth import get_admin_user, get_current_user
from app.schemas.users import UserResponse
from app.repositories.users import (
    get_users
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[UserResponse])
def get_all_users(
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != UserRole.admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    return get_users(db)


@router.delete("/{user_id}")
def delete_user(
    user_id: int, db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user)
):
    return delete_user(user_id, db)
