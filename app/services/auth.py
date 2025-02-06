from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.users import UserRole
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from app.repositories.users import get_user_by_username
from sqlalchemy.orm import Session
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    if SECRET_KEY is None or ALGORITHM is None:
        raise ValueError(
            "SECRET_KEY and ALGORITHM must be set in the env variables."
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")
        if email is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
    return {"email": email, "role": role}


def get_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != UserRole.admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    print(password)
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    if (
        SECRET_KEY is None
        or ALGORITHM is None
        or ACCESS_TOKEN_EXPIRE_MINUTES is None
    ):
        raise ValueError("Missing required environment variables.")

    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    try:
        encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        raise ValueError(f"Error encoding the token: {str(e)}")
    return encoded_token
