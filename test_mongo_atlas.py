# test_mongo_atlas.py
from pymongo import MongoClient
import time

def test_atlas_connection():
    # Your MongoDB Atlas URI with database name
    uri = "mongodb+srv://kanishkmehto7:pkkanidou@cluster0.imdjxg0.mongodb.net/qcommerce?retryWrites=true&w=majority"
    
    print("Testing MongoDB Atlas connection...")
    print(f"URI: {uri}")
    
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        
        # Test the connection
        print("Pinging database...")
        client.admin.command('ping')
        print("✅ MongoDB Atlas connection successful!")
        
        # Get database info
        db = client.get_database()
        print(f"Connected to database: {db.name}")
        
        # List collections
        collections = db.list_collection_names()
        print(f"Collections: {collections}")
        
        # Create users collection if it doesn't exist
        if 'users' not in collections:
            print("Creating 'users' collection...")
            db.create_collection('users')
            print("✅ 'users' collection created")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB Atlas connection failed: {e}")
        print("\n💡 TROUBLESHOOTING:")
        print("1. Make sure your IP is whitelisted in MongoDB Atlas")
        print("2. Check if the database name 'qcommerce' exists")
        print("3. Verify your username/password")
        return False

if __name__ == "__main__":
    test_atlas_connection()