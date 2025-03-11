from flask import Flask
from routes.plaid_routes import plaid_bp
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Register routes
    app.register_blueprint(plaid_bp, url_prefix="/plaid")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
