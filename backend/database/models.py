# backend/database/models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255))
    full_name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bank_accounts = db.relationship('BankAccount', backref='user', lazy=True)
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plaid_account_id = db.Column(db.String(255), unique=True, nullable=False)
    institution_name = db.Column(db.String(255))
    account_name = db.Column(db.String(255))
    account_type = db.Column(db.String(50))
    balance = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    transactions = db.relationship('Transaction', backref='bank_account', lazy=True)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    plaid_transaction_id = db.Column(db.String(255), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    plaid_category_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    transactions = db.relationship('Transaction', backref='category', lazy=True)
