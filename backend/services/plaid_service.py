from plaid.api import plaid_api
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.products import Products
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from datetime import datetime, timedelta
from plaid import Configuration, ApiClient
import os
from dotenv import load_dotenv

class PlaidService:
    def __init__(self):
        load_dotenv()
        configuration = Configuration(
            host="https://sandbox.plaid.com",  # Change to "https://development.plaid.com" for development
            api_key={
                "clientId": os.getenv("PLAID_CLIENT_ID"),
                "secret": os.getenv("PLAID_SECRET"),
            }
        )
        api_client = ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)

    def create_sandbox_link_token(self, user_id: str):
        """Create a link token for sandbox testing"""
        try:
            request = {
                "user": {"client_user_id": user_id},
                "client_name": "SpendApp",
                "products": ["transactions"],
                "country_codes": ["US"],
                "language": "en"
            }
            response = self.client.link_token_create(request)
            return response["link_token"]
        except Exception as e:
            print(f"Error creating link token: {str(e)}")
            raise

    def exchange_public_token(self, public_token: str):
        """Exchange public token for access token"""
        try:
            exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
            exchange_response = self.client.item_public_token_exchange(exchange_request)
            return exchange_response["access_token"]
        except Exception as e:
            print(f"Error exchanging public token: {str(e)}")
            raise

    def get_transactions(self, access_token: str, start_date: datetime = None, end_date: datetime = None):
        """Get transactions for a given access token"""
        try:
            if not start_date:
                start_date = datetime.now() - timedelta(days=30)
            if not end_date:
                end_date = datetime.now()

            options = TransactionsGetRequestOptions(
                count=100,
                offset=0
            )

            request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date.date(),
                end_date=end_date.date(),
                options=options
            )

            response = self.client.transactions_get(request)
            return response["transactions"]
        except Exception as e:
            print(f"Error getting transactions: {str(e)}")
            raise

    def get_accounts(self, access_token: str):
        """Get accounts for a given access token"""
        try:
            response = self.client.accounts_get({"access_token": access_token})
            return response["accounts"]
        except Exception as e:
            print(f"Error getting accounts: {str(e)}")
            raise

    def get_balance(self, access_token: str):
        """Get account balances for a given access token"""
        try:
            response = self.client.accounts_balance_get({"access_token": access_token})
            return response["accounts"]
        except Exception as e:
            print(f"Error getting balances: {str(e)}")
            raise


