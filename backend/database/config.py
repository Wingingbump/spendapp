# backend/database/config.py
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    """Base configuration."""
    # PostgreSQL connection URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:password@db:5432/spendapp'
    )
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # Plaid configuration
    PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
    PLAID_SECRET = os.getenv('PLAID_SECRET')
    PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')

