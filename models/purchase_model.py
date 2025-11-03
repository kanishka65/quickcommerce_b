# models/purchase_model.py
from extensions import mongo
from bson.objectid import ObjectId
import traceback

def insert_purchases(purchases_list):
    """
    Inserts a list of purchase documents into the 'purchases' collection.
    """
    if not purchases_list:
        return {"inserted": 0, "errors": 0}
    
    try:
        # 'ordered=False' allows inserts to continue even if one doc fails
        result = mongo.db.purchases.insert_many(purchases_list, ordered=False)
        return {"inserted": len(result.inserted_ids), "errors": 0}
    except Exception as e:
        print(f"Error inserting purchases: {e}")
        # This catch is basic; a real app might report duplicates
        return {"inserted": 0, "errors": len(purchases_list)}

def find_purchases_for_user(user_id_str):
    """
    Finds all purchases for a given user ID.
    It links purchases by the user's email, as defined in csv_service.py.
    """
    try:
        # 1. Find the user by their _id (which is the JWT identity)
        user = mongo.db.users.find_one(
            {"_id": ObjectId(user_id_str)},
            {"email": 1} # Only fetch the email field
        )
        
        if not user:
            print(f"No user found for ID: {user_id_str}")
            return []
        
        user_email = user.get("email")
        if not user_email:
            print(f"User {user_id_str} has no email.")
            return []

        # 2. Find purchases matching that email, sorted by most recent
        purchases = list(mongo.db.purchases.find(
            {"user": user_email}
        ).sort("order_datetime", -1))
        
        return purchases
        
    except Exception as e:
        print(f"Error finding purchases for user {user_id_str}: {e}")
        print(traceback.format_exc())
        return []

def get_purchase_stats(user_id_str):
    """
    Calculates aggregate statistics for a user, linking via user email.
    """
    try:
        # 1. Find the user's email from their ID
        user = mongo.db.users.find_one(
            {"_id": ObjectId(user_id_str)},
            {"email": 1}
        )
        
        if not user or not user.get("email"):
            return {"error": "User not found or has no email"}
        
        user_email = user["email"]
        
        # 2. Run aggregation pipeline on 'purchases' collection
        pipeline = [
            {
                "$match": {"user": user_email}
            },
            {
                "$group": {
                    "_id": "$category",
                    "total_spent": {"$sum": "$total_amount"},
                    "total_orders": {"$sum": 1}
                }
            },
            {
                "$sort": {"total_spent": -1}
            },
            {
                "$group": {
                    "_id": None, # Group all categories together
                    "total_spent_overall": {"$sum": "$total_spent"},
                    "total_orders_overall": {"$sum": "$total_orders"},
                    "category_breakdown": {
                        "$push": {
                            "category": "$_id",
                            "total_spent": "$total_spent",
                            "total_orders": "$total_orders"
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0, # Remove the _id field
                    "total_spent": "$total_spent_overall",
                    "total_orders": "$total_orders_overall",
                    "average_order_value": {
                        "$cond": [
                            {"$eq": ["$total_orders_overall", 0]}, 
                            0, 
                            {"$divide": ["$total_spent_overall", "$total_orders_overall"]}
                        ]
                    },
                    "category_breakdown": "$category_breakdown"
                }
            }
        ]
        
        stats = list(mongo.db.purchases.aggregate(pipeline))
        
        if not stats:
            # Return empty stats if no purchases found
            return {
                "total_spent": 0,
                "total_orders": 0,
                "average_order_value": 0,
                "category_breakdown": []
            }
        
        return stats[0] # Aggregation returns a list with one doc

    except Exception as e:
        print(f"Error getting purchase stats for user {user_id_str}: {e}")
        print(traceback.format_exc())
        return {"error": str(e)}