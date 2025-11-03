import os

class Config:
    MONGO_URI = os.environ.get("MONGO_URI")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
