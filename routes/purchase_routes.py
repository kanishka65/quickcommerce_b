# routes/purchase_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.purchase_model import insert_purchases, find_purchases_for_user, get_purchase_stats

# --- New Imports ---
from services.csv_service import parse_purchase_csv
from extensions import mongo
from bson.objectid import ObjectId
import traceback
# --- End New Imports ---


purchase_bp = Blueprint("purchase_bp", __name__)

@purchase_bp.route("/upload-csv", methods=["POST"])
@jwt_required()
def upload_csv():
    try:
        # --- Updated Logic ---
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if file and file.filename.endswith('.csv'):
            user_id = get_jwt_identity()
            
            # Get user's email to tag purchases (as defined in csv_service)
            user = mongo.db.users.find_one(
                {"_id": ObjectId(user_id)}, 
                {"email": 1}
            )
            
            if not user or not user.get("email"):
                return jsonify({"error": "User not found or email missing"}), 404
            
            user_email = user["email"]
            
            # Parse the CSV stream using your service
            purchases_data = parse_purchase_csv(file.stream, user_email)
            
            if not purchases_data:
                return jsonify({"error": "Failed to parse CSV or CSV is empty"}), 400
            
            # Insert data into the database using your new model
            result = insert_purchases(purchases_data)
            
            return jsonify({
                "message": "File processed successfully",
                "inserted": result.get("inserted", 0),
                "skipped": 0, # You can add skip logic in the model if needed
                "errors": result.get("errors", 0)
            }), 201
        else:
            return jsonify({"error": "Invalid file type. Please upload a .csv file"}), 400
        # --- End Updated Logic ---

    except Exception as e:
        print(traceback.format_exc()) # Print full traceback for debugging
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@purchase_bp.route("/list", methods=["GET"])
@jwt_required()
def list_purchases():
    try:
        user_id = get_jwt_identity()
        purchases = find_purchases_for_user(user_id)
        
        # Convert ObjectId and datetime to string for JSON serialization
        for purchase in purchases:
            purchase['_id'] = str(purchase['_id'])
            # Convert datetime objects to ISO format string
            if purchase.get('order_datetime') and hasattr(purchase['order_datetime'], 'isoformat'):
                purchase['order_datetime'] = purchase['order_datetime'].isoformat()
            
        return jsonify({
            "purchases": purchases,
            "total": len(purchases)
        }), 200
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@purchase_bp.route("/stats", methods=["GET"])
@jwt_required()
def purchase_stats():
    try:
        user_id = get_jwt_identity()
        stats = get_purchase_stats(user_id)
        return jsonify(stats), 200
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500