from flask import Blueprint, request, jsonify
from services.plaid_service import PlaidService
from database.models import db, User, BankAccount, Transaction
from datetime import datetime

plaid_bp = Blueprint('plaid', __name__)
plaid_service = PlaidService()

@plaid_bp.route('/create-link-token', methods=['POST'])
def create_link_token():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        
        link_token = plaid_service.create_sandbox_link_token(user_id)
        return jsonify({"link_token": link_token})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@plaid_bp.route('/exchange-token', methods=['POST'])
def exchange_token():
    try:
        data = request.get_json()
        public_token = data.get('public_token')
        user_id = data.get('user_id')
        
        if not public_token or not user_id:
            return jsonify({"error": "public_token and user_id are required"}), 400
        
        # Exchange public token for access token
        access_token = plaid_service.exchange_public_token(public_token)
        
        # Get account information
        accounts = plaid_service.get_accounts(access_token)
        
        # Store bank account information
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        for account in accounts:
            bank_account = BankAccount(
                user_id=user_id,
                plaid_account_id=account['account_id'],
                institution_name=account.get('institution_name', 'Unknown'),
                account_name=account.get('name', 'Unknown'),
                account_type=account.get('type', 'Unknown'),
                balance=account.get('balances', {}).get('current', 0)
            )
            db.session.add(bank_account)
        
        db.session.commit()
        return jsonify({"message": "Bank accounts added successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@plaid_bp.route('/transactions/<user_id>', methods=['GET'])
def get_user_transactions(user_id):
    try:
        # Get user's bank accounts
        bank_accounts = BankAccount.query.filter_by(user_id=user_id).all()
        if not bank_accounts:
            return jsonify({"error": "No bank accounts found for user"}), 404
        
        all_transactions = []
        for account in bank_accounts:
            transactions = plaid_service.get_transactions(account.plaid_account_id)
            for transaction in transactions:
                # Store transaction in database
                db_transaction = Transaction(
                    bank_account_id=account.id,
                    plaid_transaction_id=transaction['transaction_id'],
                    amount=transaction['amount'],
                    date=datetime.strptime(transaction['date'], '%Y-%m-%d').date(),
                    description=transaction.get('name', '')
                )
                db.session.add(db_transaction)
                all_transactions.append(transaction)
        
        db.session.commit()
        return jsonify({"transactions": all_transactions})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@plaid_bp.route('/accounts/<user_id>', methods=['GET'])
def get_user_accounts(user_id):
    try:
        bank_accounts = BankAccount.query.filter_by(user_id=user_id).all()
        if not bank_accounts:
            return jsonify({"error": "No bank accounts found for user"}), 404
        
        accounts_data = []
        for account in bank_accounts:
            accounts_data.append({
                "id": account.id,
                "name": account.account_name,
                "type": account.account_type,
                "balance": account.balance,
                "institution": account.institution_name
            })
        
        return jsonify({"accounts": accounts_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
