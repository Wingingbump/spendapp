from dotenv import load_dotenv
load_dotenv()  # Loads environment variables from .env file

import unittest
from backend.app import app
import json
import requests
import os
from unittest.mock import patch  # Make sure to import patch

# python -m unittest -k [TEST] backend.tests.test_plaid_routes

class TestPlaidRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the Flask app for testing"""
        cls.client = app.test_client()

    def test_get_link_token(self):
        """Test the /get_link_token route"""
        response = self.client.post(
            "/plaid/get_link_token",
            json={"user_id": "test_user"}
        )

        # Assert the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains a valid link_token
        response_data = response.get_json()
        self.assertIn("link_token", response_data)
        self.assertIn("expiration", response_data)
        self.link_token = response_data["link_token"]  # Store the link token for future use

    def test_exchange_public_token(self):
        """Test generating and exchanging public token"""

        # Step 1: Generate a public token using /sandbox/public_token/create
        response = self.client.post(
            "/plaid/sandbox/public_token_create",
            json={
                "institution_id": "ins_109508",  # Example institution ID (replace with valid institution)
                "initial_products": ["auth", "transactions"],
                "user_custom": "custom_user_1234"
            }
        )
        print(response)

        # Assert the response is successful and contains the public token
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        public_token = data.get("public_token")
        self.assertIsNotNone(public_token, "Public token should not be None")

        # Step 2: Exchange the generated public token for an access token
        exchange_response = self.client.post(
            "/plaid/exchange_public_token",
            json={"public_token": public_token}
        )

        # Assert that the exchange request was successful and contains an access token
        self.assertEqual(exchange_response.status_code, 200)
        exchange_data = exchange_response.get_json()
        access_token = exchange_data.get("access_token")
        self.assertIsNotNone(access_token, "Access token should not be None")
        
    def test_get_transactions(self):
        """Test fetching transactions from multiple institutions"""
        # Step 1: Create the public token
        try:
            response = self.client.post(
                "/plaid/sandbox/public_token_create",
                json={
                    "institution_id": "ins_109508",  # Example institution ID
                    "initial_products": ["auth", "transactions"],
                }
            )
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            public_token = data.get("public_token")
            self.assertIsNotNone(public_token, "Public token should not be None")
        except Exception as e:
            self.fail(f"Failed to create public token: {str(e)}")

        # Step 2: Exchange the public token for an access token
        try:
            exchange_response = self.client.post(
                "/plaid/exchange_public_token",
                json={"public_token": public_token, "user_id": "test_user"}
            )
            self.assertEqual(exchange_response.status_code, 200)
            exchange_data = exchange_response.get_json()
            access_token = exchange_data.get("access_token")
            self.assertIsNotNone(access_token, "Access token should not be None")
        except Exception as e:
            self.fail(f"Failed to exchange public token: {str(e)}")

        # Step 3: Simulate calling the endpoint to get transactions
        response = self.client.post(
            "/plaid/get_transactions",
            json={"user_id": "test_user"}  # The access token is already stored
        )

        # Debugging prints
        print(f"Response status code: {response.status_code}")  # Print status code
        print(f"Response headers: {response.headers}")  # Print response headers
        print(f"Response body: {response.data}")  # Print raw response data (useful for debugging)

        # Try to load the response data as JSON
        try:
            data = json.loads(response.data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            data = {}

        # More debugging
        if "error" in data:
            print(f"Error in response: {data['error']}")  # Print error message if present

        # Assert the response
        self.assertEqual(response.status_code, 200, f"Expected status code 200 but got {response.status_code}")
        self.assertIn("transactions", data, f"Expected 'transactions' key but got: {data}")
        self.assertGreater(len(data.get("transactions", [])), 0, "Expected at least one transaction but found none")


if __name__ == "__main__":
    unittest.main()
