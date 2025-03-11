# backend/database/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    financial_institutions = db.relationship('FinancialInstitution', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'

class FinancialInstitution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    accounts = db.relationship('Account', backref='institution', lazy=True)

    def __repr__(self):
        return f'<FinancialInstitution {self.name}>'

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(50), nullable=False)  # e.g., checking, savings
    balance = db.Column(db.Float, nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('financial_institution.id'), nullable=False)
    transactions = db.relationship('Transaction', backref='account', lazy=True)

    def __repr__(self):
        return f'<Account {self.account_type} - {self.balance}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(250), nullable=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __repr__(self):
        return f'<Transaction {self.amount} on {self.date}>'
