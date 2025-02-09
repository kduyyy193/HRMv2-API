from sqlalchemy import Column, Date, Integer, String, Boolean, Enum
from app.data_access.db import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.user)
    department = Column(String, nullable=True)
    full_name = Column(String, nullable=False)
    title = Column(String, nullable=True)
    birth_year = Column(Integer, nullable=True)
    date_joined = Column(Date, nullable=True)
    date_left = Column(Date, nullable=True)
    place_of_origin = Column(String, nullable=True) 
