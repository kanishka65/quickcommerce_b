# app.py
from flask import Flask, jsonify
from config import Config
from extensions import mongo, jwt, bcrypt
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    print("ENV MONGO_URI:", os.environ.get("MONGO_URI"))   # Check actual env
    print("Config MONGO_URI:", app.config.get("MONGO_URI"))

    # Rest of your code...

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable debug mode
    app.debug = True
    
    # Enable CORS - allow only your Vercel frontend
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

app = create_app()

if __name__ == '__main__':
    # For Render deployment, don't bind to localhost
    app.run(debug=True)
