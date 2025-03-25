import unittest
from services.plaid_service import PlaidService
from database.models import db, User, BankAccount, Transaction
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class TestPlaidIntegration(unittest.TestCase):
    def setUp(self):
        self.plaid_service = PlaidService()
        
    def test_create_link_token(self):
        """Test creating a link token"""
        user_id = "test_user"
        link_token = self.plaid_service.create_sandbox_link_token(user_id)
        self.assertIsNotNone(link_token)
        self.assertIsInstance(link_token, str)
        
    def test_exchange_public_token(self):
        """Test exchanging a public token for an access token"""
        # Create a sandbox public token
        public_token = self.plaid_service.create_sandbox_link_token("test_user")
        access_token = self.plaid_service.exchange_public_token(public_token)
        self.assertIsNotNone(access_token)
        self.assertIsInstance(access_token, str)
        
    def test_get_transactions(self):
        """Test retrieving transactions"""
        # Create a sandbox public token and exchange it
        public_token = self.plaid_service.create_sandbox_link_token("test_user")
        access_token = self.plaid_service.exchange_public_token(public_token)
        
        # Get transactions for the last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        transactions = self.plaid_service.get_transactions(
            access_token,
            start_date=start_date,
            end_date=end_date
        )
        
        self.assertIsNotNone(transactions)
        self.assertIsInstance(transactions, list)
        
    def test_get_accounts(self):
        """Test retrieving account information"""
        # Create a sandbox public token and exchange it
        public_token = self.plaid_service.create_sandbox_link_token("test_user")
        access_token = self.plaid_service.exchange_public_token(public_token)
        
        accounts = self.plaid_service.get_accounts(access_token)
        self.assertIsNotNone(accounts)
        self.assertIsInstance(accounts, list)
        
    def test_get_balance(self):
        """Test retrieving account balances"""
        # Create a sandbox public token and exchange it
        public_token = self.plaid_service.create_sandbox_link_token("test_user")
        access_token = self.plaid_service.exchange_public_token(public_token)
        
        balances = self.plaid_service.get_balance(access_token)
        self.assertIsNotNone(balances)
        self.assertIsInstance(balances, list)

if __name__ == '__main__':
    unittest.main() 