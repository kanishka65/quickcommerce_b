# simple helpers for user queries
from extensions import mongo
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(email, password, name=None):
    hashed = generate_password_hash(password)
    user = {"email": email, "password": hashed, "name": name or "", "created_at": __import__("datetime").datetime.utcnow()}
    mongo.db.users.insert_one(user)
    return user

def find_user_by_email(email):
    return mongo.db.users.find_one({"email": email})

def verify_password(stored_hash, password):
    return check_password_hash(stored_hash, password)
