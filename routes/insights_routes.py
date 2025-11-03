# routes/insights_routes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.analytics_service import build_monthly_summary, build_heatmap_matrix, replenishment_suggestions, get_spending_trends

insights_bp = Blueprint("insights_bp", __name__)

@insights_bp.route("/summary", methods=["GET"])
@jwt_required()
def summary():
    try:
        user_id = get_jwt_identity()
        print(f"Getting summary for user: {user_id}")
        
        summary_data = build_monthly_summary(user_id)
        
        return jsonify(summary_data), 200
    except Exception as e:
        print(f"Error in summary endpoint: {e}")
        return jsonify({"error": "Failed to get summary data"}), 500

@insights_bp.route("/heatmap", methods=["GET"])
@jwt_required()
def heatmap():
    try:
        user_id = get_jwt_identity()
        print(f"Getting heatmap for user: {user_id}")
        
        matrix = build_heatmap_matrix(user_id)
        flat_matrix = [item for sublist in matrix for item in sublist]
        
        response_data = {
            "matrix": matrix,
            "max": max(flat_matrix) if flat_matrix else 0,
            "min": min(flat_matrix) if flat_matrix else 0,
            "average": sum(flat_matrix) // len(flat_matrix) if flat_matrix else 0
        }
        
        return jsonify(response_data), 200
    except Exception as e:
        print(f"Error in heatmap endpoint: {e}")
        return jsonify({"error": "Failed to get heatmap data"}), 500

@insights_bp.route("/trends", methods=["GET"])
@jwt_required()
def trends():
    try:
        user_id = get_jwt_identity()
        print(f"Getting trends for user: {user_id}")
        
        monthly_spend = get_spending_trends(user_id)
        
        trend_data = {
            "monthly_spend": monthly_spend,
            "category_trends": [
                {"category": "dairy", "trend": "up", "change": 15},
                {"category": "snacks", "trend": "down", "change": -8},
                {"category": "beverages", "trend": "up", "change": 22}
            ]
        }
        
        return jsonify(trend_data), 200
    except Exception as e:
        print(f"Error in trends endpoint: {e}")
        return jsonify({"error": "Failed to get trend data"}), 500

@insights_bp.route("/suggestions", methods=["GET"])
@jwt_required()
def suggestions():
    try:
        user_id = get_jwt_identity()
        print(f"Getting suggestions for user: {user_id}")
        
        suggestions_data = replenishment_suggestions(user_id)
        
        return jsonify({"suggestions": suggestions_data}), 200
    except Exception as e:
        print(f"Error in suggestions endpoint: {e}")
        return jsonify({"error": "Failed to get suggestions"}), 500