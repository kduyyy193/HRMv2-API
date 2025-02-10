from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.data_access.db import SessionLocal
from app.models.users import UserRole
from app.services.auth import get_admin_user, get_current_user
from app.schemas.users import UserResponse
from app.repositories.users import (
    count_users,
    delete_user_by_id,
    get_users,
    update_user_by_id
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
        current_user: dict = Depends(get_current_user),
        skip: int = Query(0, alias="page", ge=0),
        limit: int = Query(10, alias="size", le=100)
):
    if current_user["role"] != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    users = get_users(db, skip=skip * limit, limit=limit)
    total_users = count_users(db)

    return {
        "total_count": total_users,
        "page": skip,
        "size": limit,
        "data": users
    }


@router.post("/{user_id}")
def update_user(
    user_id: int,
    updates: dict,
    db: Session = Depends(get_db)
):
    return update_user_by_id(db, user_id, updates)


@router.delete("/{user_id}")
def delete_user(
    user_id: int, db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user)
):
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    return delete_user_by_id(db, user_id)
