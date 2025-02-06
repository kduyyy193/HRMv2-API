from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users
from app.data_access.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI User Management")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["Users"])


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI User Management"}
