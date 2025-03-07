import requests
import os
from datetime import datetime, timedelta

PLAID_API_URL = f"https://{os.getenv('PLAID_ENV')}.plaid.com"

def create_link_token(user_id):
    """Generates a link token to initialize Plaid Link."""
    url = f"{PLAID_API_URL}/link/token/create"
    
    payload = {
        "client_id": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET"),
        "client_name": "SpendApp",
        "user": {"client_user_id": user_id},
        "products": ["transactions"],  # To retrieve transactions
        "country_codes": ["US"],
        "language": "en"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Will raise an error for bad responses
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return {"error": str(err)}
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")
        return {"error": str(err)}

def exchange_public_token(public_token):
    """Exchanges a public token for an access token."""
    url = f"{PLAID_API_URL}/item/public_token/exchange"

    payload = {
        "client_id": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET"),
        "public_token": public_token
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Will raise an exception for 4xx and 5xx status codes
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        print(f"Response body: {response.text}")  # Print the full response for more details
        return {"error": str(err)}
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")
        return {"error": str(err)}


def get_transactions(access_token):
    """Fetches transactions for the given access token."""
    url = f"{PLAID_API_URL}/transactions/get"
    
    # Setting the date range (last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    payload = {
        "access_token": access_token,
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
    }

    headers = {
        "Plaid-Client-ID": os.getenv("PLAID_CLIENT_ID"),
        "Plaid-Secret": os.getenv("PLAID_SECRET")
    }
    
    # Debugging: Print out the payload being sent to Plaid API
    print(f"Sending request to Plaid with payload: {payload}")
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        # Debugging: Print out the response from Plaid
        print(f"Response from Plaid: {response.json()}")
        
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return {"error": str(err)}
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")
        return {"error": str(err)}


