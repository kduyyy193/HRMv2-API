from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.users import UserRole
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Security(oauth2_scheme)):
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
