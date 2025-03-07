from flask import Blueprint, request, jsonify
from backend.services.plaid_service import create_link_token, exchange_public_token, get_transactions
import requests
import os

plaid_bp = Blueprint("plaid", __name__)

USER_ACCESS_TOKENS = {}  # Temporary storage for tokens

PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")

# Endpoint to create the link token for user
@plaid_bp.route("/get_link_token", methods=["POST"])
def get_link_token():
    """Creates a link token for the user to select a bank."""
    user_id = request.json.get("user_id", "test_user")
    response = create_link_token(user_id)
    return jsonify(response)

# Endpoint to generate a public token in sandbox
@plaid_bp.route("/sandbox/public_token_create", methods=["POST"])
def create_public_token():
    """Create a test public token using Plaid's sandbox API."""
    institution_id = request.json.get("institution_id")
    initial_products = request.json.get("initial_products", ["auth", "transactions"])
    
    # Call Plaid API to create the public token
    url = f"https://{PLAID_ENV}.plaid.com/sandbox/public_token/create"
    
    payload = {
        "institution_id": institution_id,
        "initial_products": initial_products
    }
    
    headers = {
        "Content-Type": "application/json",
        "Plaid-Client-ID": PLAID_CLIENT_ID,
        "Plaid-Secret": PLAID_SECRET,
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()

    if response.status_code != 200:
        return jsonify({"error": response_data.get("error_message", "Failed to create public token")}), 400

    return jsonify({"public_token": response_data.get("public_token")})

# Endpoint to exchange the public token for an access token
@plaid_bp.route("/exchange_public_token", methods=["POST"])
def get_access_token():
    """Exchanges public token for an access token."""
    user_id = request.json.get("user_id", "test_user")
    public_token = request.json.get("public_token")

    response = exchange_public_token(public_token)

    if "access_token" in response:
        USER_ACCESS_TOKENS[user_id] = response["access_token"]

    return jsonify(response)

# Endpoint to retrieve user transactions
@plaid_bp.route("/get_transactions", methods=["POST"])
def get_user_transactions():
    """Retrieves transactions for the user from all linked institutions."""
    user_id = request.json.get("user_id", "test_user")
    
    if user_id not in USER_ACCESS_TOKENS:
        return jsonify({"error": "Access token not found for user."}), 400
    
    access_token = USER_ACCESS_TOKENS[user_id]
    
    # Get transactions for the user
    transactions = get_transactions(access_token)
    
    return jsonify(transactions)
