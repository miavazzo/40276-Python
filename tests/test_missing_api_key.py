import unittest
import json
from app import create_app

class TestMissingApiKey(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_missing_api_key(self):
        payload = {
            "client_id": "your_client_id",
            "client_secret": "your_client_secret",
            "tenant_id": "your_tenant_id",
            "username": "your_username",
            "subject": "Test Subject",
            "body": "Test Body",
            "to_emails": ["test@example.com"]
        }
        response = self.client.post('/send_email', json=payload)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
