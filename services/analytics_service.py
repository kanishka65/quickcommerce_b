# services/analytics_service.py
from extensions import mongo
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import random

def build_monthly_summary(user_id):
    """
    Build monthly summary statistics for a user
    In a real app, this would query the database
    For now, return mock data
    """
    try:
        # Mock data - replace with actual MongoDB aggregation later
        summary = {
            "total_spend": 3920.50,
            "avg_order_value": 245.60,
            "total_orders": 16,
            "by_category": [
                {"key": "dairy", "total": 870, "count": 8},
                {"key": "snacks", "total": 640, "count": 12},
                {"key": "beverages", "total": 450, "count": 6},
                {"key": "produce", "total": 320, "count": 5}
            ],
            "budget": {"set": 4000, "spent": 3920.50, "remaining": 79.50, "percent": 98}
        }
        return summary
    except Exception as e:
        print(f"Error building monthly summary: {e}")
        return {}

def build_heatmap_matrix(user_id):
    """
    Build heatmap data for user spending patterns
    Returns a 7x24 matrix (days x hours)
    """
    try:
        # Generate realistic-looking heatmap data
        matrix = []
        for day in range(7):  # 7 days of week
            day_data = []
            for hour in range(24):  # 24 hours
                # Generate data with realistic patterns
                if 8 <= hour <= 20:  # Daytime hours
                    base_value = random.randint(50, 300)
                else:  # Nighttime hours
                    base_value = random.randint(0, 100)
                
                # Weekend boost
                if day >= 5:  # Saturday (5) and Sunday (6)
                    base_value += random.randint(50, 150)
                
                # Evening peak (5 PM - 8 PM)
                if 17 <= hour <= 19:
                    base_value += random.randint(80, 120)
                
                # Lunch peak (12 PM - 2 PM)
                if 12 <= hour <= 14:
                    base_value += random.randint(60, 100)
                
                day_data.append(base_value)
            matrix.append(day_data)
        
        return matrix
    except Exception as e:
        print(f"Error building heatmap matrix: {e}")
        # Return empty matrix on error
        return [[0 for _ in range(24)] for _ in range(7)]

def replenishment_suggestions(user_id):
    """
    Generate replenishment suggestions based on purchase history
    """
    try:
        # Mock suggestions - replace with actual logic later
        suggestions = [
            {
                "category": "dairy",
                "item": "Milk",
                "predicted_days_left": 2,
                "suggestion": "Time to restock",
                "priority": "high"
            },
            {
                "category": "snacks",
                "item": "Chips",
                "predicted_days_left": 5,
                "suggestion": "Consider buying soon",
                "priority": "medium"
            },
            {
                "category": "beverages", 
                "item": "Coffee",
                "predicted_days_left": 7,
                "suggestion": "You're good for now",
                "priority": "low"
            }
        ]
        return suggestions
    except Exception as e:
        print(f"Error generating replenishment suggestions: {e}")
        return []

def get_spending_trends(user_id, months=6):
    """
    Get spending trends over time
    """
    try:
        # Mock trend data
        monthly_data = []
        base_spend = 3000
        for i in range(months):
            month_name = (datetime.now() - timedelta(days=30*i)).strftime('%b')
            spend = base_spend + random.randint(-500, 500)
            monthly_data.append({
                "month": month_name,
                "spend": spend
            })
        
        monthly_data.reverse()  # Show oldest to newest
        
        return monthly_data
    except Exception as e:
        print(f"Error getting spending trends: {e}")
        return []