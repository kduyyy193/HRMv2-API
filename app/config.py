class Settings:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    SECRET_KEY = "your-secret-key9902"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30    # min


settings = Settings()
