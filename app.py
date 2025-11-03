# app.py
import os
from flask import Flask, jsonify
from config import Config
from extensions import mongo, jwt, bcrypt
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable debug mode (optional on Render, can turn off later)
    app.debug = True
    
    # Enable CORS for your Vercel frontend
    CORS(app, origins=["https://quickcommerce-f.vercel.app"])
    
    print("Initializing MongoDB connection...")
    print(f"MongoDB URI: {app.config['MONGO_URI']}")
    
    # Initialize extensions
    try:
        mongo.init_app(app)
        print("✅ MongoDB initialized successfully")
        
        # Test the connection
        with app.app_context():
            mongo.db.command('ping')
            print("✅ MongoDB connection test passed")
            
    except Exception as e:
        print(f"❌ MongoDB initialization failed: {e}")
    
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.purchase_routes import purchase_bp
    from routes.insights_routes import insights_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(purchase_bp, url_prefix='/purchases')
    app.register_blueprint(insights_bp, url_prefix='/insights')
    
    # Test route
    @app.route('/')
    def hello():
        return jsonify({"message": "Q-Commerce Backend is running!"})
    
    return app

# Create the app
app = create_app()

# Only run locally with Flask
if __name__ == '__main__':
    # Use host='0.0.0.0' so Render can access it
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
