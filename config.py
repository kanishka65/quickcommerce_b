# config.py
import os

class Config:
    # Your working MongoDB Atlas URI
    MONGO_URI = "mongodb+srv://kanishkmehto7:pkkanidou@cluster0.imdjxg0.mongodb.net/qcommerce?retryWrites=true&w=majority"
    
    # JWT Secret Key
    JWT_SECRET_KEY = "super-secret-key"
    
    # Flask secret key
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret")
    
    # Upload size limit
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024