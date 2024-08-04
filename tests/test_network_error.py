import unittest
from unittest.mock import patch
from app import create_app
import requests

class TestNetworkError(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch('app.email_service.requests.post', side_effect=requests.exceptions.RequestException)
    def test_network_error(self, mock_post):
        payload = {
            "client_id": "your_client_id",
            "client_secret": "your_client_secret",
            "tenant_id": "your_tenant_id",
            "username": "your_username",
            "subject": "Test Subject",
            "body": "Test Body",
            "to_emails": ["test@example.com"]
        }
        response = self.client.post('/send_email', headers={'x-api-key': 'your_api_key'}, json=payload)
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
