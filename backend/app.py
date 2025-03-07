import os
import datetime
from flask import Flask, jsonify
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid import Configuration, ApiClient, Environment
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set up Plaid API client
configuration = Configuration(
    host=Environment.Sandbox,  # Change to Development or Production if needed
    api_key={
        "clientId": os.getenv('PLAID_CLIENT_ID'),
        "secret": os.getenv('PLAID_SECRET')
    }
)
api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# Route to fetch user transaction data
@app.route('/transactions/<access_token>', methods=['GET'])
def get_transactions(access_token):
    try:
        start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).date()
        end_date = datetime.datetime.now().date()

        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date,
            options=TransactionsGetRequestOptions(count=10)  # Fetch the last 10 transactions
        )

        response = client.transactions_get(request)

        transactions = response.to_dict()['transactions']  # Convert to dictionary before returning JSON
        return jsonify(transactions), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
