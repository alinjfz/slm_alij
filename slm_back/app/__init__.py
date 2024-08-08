from flask import Flask
from app.routes import main
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://localhost:3001"], "supports_credentials": True}})
    
    return app
