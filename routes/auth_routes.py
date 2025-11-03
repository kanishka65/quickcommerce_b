# routes/auth_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from extensions import mongo, bcrypt
from bson import ObjectId
import datetime
import sys
import traceback

# --- FIX: Define the blueprint *before* any routes ---
auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        print("=== REGISTRATION START ===")
        
        # Get JSON data
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400
            
        data = request.get_json()
        print("Raw data received:", data)
        
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
            
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")
        
        print(f"Extracted - Name: {name}, Email: {email}, Password: {'*' * len(password) if password else 'None'}")

        # Validation
        if not email:
            return jsonify({"error": "Email is required"}), 400
        if not password:
            return jsonify({"error": "Password is required"}), 400

        print("Checking for existing user...")
        # Check if user already exists
        existing_user = mongo.db.users.find_one({"email": email})
        if existing_user:
            print("User already exists")
            return jsonify({"error": "User already exists"}), 409

        print("Hashing password...")
        # Hash password
        hashed_password = bcrypt.generate_password_hash(password)
        
        user_data = {
            "email": email,
            "password": hashed_password,
            "name": name or email.split('@')[0],
            "created_at": datetime.datetime.utcnow()
        }
        
        print("Inserting user into MongoDB...")
        # Insert user
        result = mongo.db.users.insert_one(user_data)
        user_id = str(result.inserted_id)
        print(f"User inserted with ID: {user_id}")
        
        print("Creating JWT tokens...")
        # Create tokens
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        
        response_data = {
            "message": "User registered successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user_id,
                "email": email,
                "name": user_data["name"]
            }
        }
        
        print("=== REGISTRATION SUCCESS ===")
        return jsonify(response_data), 201
        
    except Exception as e:
        print("=== REGISTRATION ERROR ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        print("=== LOGIN ATTEMPT ===")
        print("Received data:", data)
        
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
            
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        # Find user in MongoDB
        print("Looking for user in MongoDB...")
        user = mongo.db.users.find_one({"email": email})
        if not user:
            print("User not found")
            return jsonify({"error": "Invalid credentials"}), 401

        # Check password
        print("Checking password...")
        if not bcrypt.check_password_hash(user["password"], password):
            print("Password incorrect")
            return jsonify({"error": "Invalid credentials"}), 401

        # Create tokens
        user_id = str(user["_id"])
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        
        response_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user_id,
                "email": user["email"],
                "name": user.get("name", user["email"].split('@')[0])
            }
        }
        
        print("=== LOGIN SUCCESSFUL ===")
        print("Response:", response_data)
        return jsonify(response_data), 200
        
    except Exception as e:
        print("=== LOGIN ERROR ===")
        print("Error:", str(e))
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user_id = get_jwt_identity()
        user = mongo.db.users.find_one({"_id": ObjectId(current_user_id)})
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        new_access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            "access_token": new_access_token,
            "user": {
                "id": str(user["_id"]),
                "email": user["email"],
                "name": user.get("name", user["email"].split('@')[0])
            }
        }), 200
        
    except Exception as e:
        print("Refresh error:", str(e))
        return jsonify({"error": "Invalid token"}), 401


# Debug endpoint to see MongoDB users
@auth_bp.route("/debug-users", methods=["GET"])
def debug_users():
    try:
        users = list(mongo.db.users.find({}, {"password": 0}))  # Exclude passwords
        for user in users:
            user["_id"] = str(user["_id"])
        
        return jsonify({
            "total_users": len(users),
            "users": users
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Test endpoint
@auth_bp.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Auth routes are working!"}), 200