from dotenv import load_dotenv
load_dotenv()  # Loads environment variables from .env file
import unittest
import os
from unittest.mock import patch, Mock
from backend.services.plaid_service import get_transactions  # Update with the correct import path
from datetime import datetime, timedelta  # Make sure timedelta is imported

class TestPlaidService(unittest.TestCase):
    
    @patch('backend.services.plaid_service.requests.post')  # Mock the requests.post call
    def test_get_transactions(self, mock_post):
        """Test fetching transactions from Plaid"""

        # Mock the response that Plaid would return
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "transactions": [
                {"id": "1", "date": "2025-02-01", "amount": 100},
                {"id": "2", "date": "2025-02-02", "amount": 50},
            ]
        }
        
        # Configure the mock to return the mocked response
        mock_post.return_value = mock_response

        # Test the get_transactions function
        access_token = "test-access-token"
        result = get_transactions(access_token)

        # Assertions
        mock_post.assert_called_once_with(
            "https://sandbox.plaid.com/transactions/get",  # Ensure it calls the correct URL
            json={
                "access_token": access_token,
                "start_date": (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                "end_date": datetime.now().strftime('%Y-%m-%d'),
            },
            headers={"Plaid-Client-ID": os.getenv("PLAID_CLIENT_ID"), "Plaid-Secret": os.getenv("PLAID_SECRET")}  # Ensure the correct headers
        )
        
        self.assertEqual(result.get("transactions")[0]["amount"], 100)  # Check if the returned amount is correct
        self.assertGreater(len(result.get("transactions")), 0)  # Ensure transactions are returned

if __name__ == '__main__':
    unittest.main()
