from plaid.api import plaid_api
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.products import Products
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
import os
from dotenv import load_dotenv

# Configure Plaid client
from plaid import Configuration, ApiClient
# Load environment variables
load_dotenv()

configuration = Configuration(
    host="https://sandbox.plaid.com",
    api_key={
        "clientId": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET"),
    }
)

api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# Step 1: Create a sandbox public token
sandbox_request = SandboxPublicTokenCreateRequest(
    institution_id="ins_109508",  # First Platypus Bank
    initial_products=[Products("transactions")]  # Correct way to pass Products
)
sandbox_response = client.sandbox_public_token_create(sandbox_request)
public_token = sandbox_response["public_token"]

# Step 2: Exchange the public token for an access token
exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
exchange_response = client.item_public_token_exchange(exchange_request)

access_token = exchange_response["access_token"]
print(f"Sandbox Access Token: {access_token}")
