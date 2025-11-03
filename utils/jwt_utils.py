# optional helpers; not strictly required but useful
from flask_jwt_extended import get_jwt_identity
def current_user_email():
    try:
        return get_jwt_identity()
    except Exception:
        return None
