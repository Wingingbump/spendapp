from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from database.models import db, User, BankAccount, Transaction, Category
from database.config import Config
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

load_dotenv()

def get_date_range(time_period):
    now = datetime.utcnow()
    if time_period == 'month':
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif time_period == 'ytd':
        start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    elif time_period == 'year':
        start_date = now.replace(year=now.year - 1, hour=0, minute=0, second=0, microsecond=0)
    else:
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return start_date, now

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/spendapp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this in production
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
    
    # Initialize CORS with specific configuration
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "expose_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize database
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Register blueprints
    from routes import main, auth
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.router)  # Remove url_prefix to match frontend
    
    jwt = JWTManager(app)
    
    return app

app = create_app()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'detail': 'Email already registered'}), 400
        
    user = User(
        email=data['email'],
        full_name=data.get('fullName'),
        hashed_password=generate_password_hash(data['password'])
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password_hash(user.hashed_password, data['password']):
        return jsonify({'detail': 'Invalid email or password'}), 401
        
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name
        }
    })

@app.route('/api/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'detail': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'full_name': user.full_name
    })

@app.route('/api/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    time_period = request.args.get('time_period', 'month')
    start_date, end_date = get_date_range(time_period)
    
    # Get all bank accounts for the user
    bank_accounts = BankAccount.query.filter_by(user_id=user_id).all()
    account_ids = [account.id for account in bank_accounts]
    
    # Get transactions for the specified time period
    transactions = Transaction.query.filter(
        Transaction.bank_account_id.in_(account_ids),
        Transaction.date.between(start_date, end_date)
    ).order_by(Transaction.date.desc()).all()
    
    return jsonify([{
        'id': t.id,
        'date': t.date.isoformat(),
        'description': t.description,
        'amount': t.amount,
        'category': t.category,
        'merchant': t.merchant
    } for t in transactions])

@app.route('/api/summary', methods=['GET'])
@jwt_required()
def get_summary():
    user_id = get_jwt_identity()
    time_period = request.args.get('time_period', 'month')
    start_date, end_date = get_date_range(time_period)
    
    # Get all bank accounts for the user
    bank_accounts = BankAccount.query.filter_by(user_id=user_id).all()
    account_ids = [account.id for account in bank_accounts]
    
    # Get transactions for the specified time period
    transactions = Transaction.query.filter(
        Transaction.bank_account_id.in_(account_ids),
        Transaction.date.between(start_date, end_date)
    ).all()
    
    # Calculate summary
    income = sum(t.amount for t in transactions if t.amount > 0)
    expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)
    net = income - expenses
    
    return jsonify({
        'income': income,
        'expenses': expenses,
        'net': net,
        'period': {
            'start': start_date.isoformat(),
            'end': end_date.isoformat()
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
