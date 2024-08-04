import unittest
import json
from app import create_app

class TestInvalidRecipientEmail(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_invalid_recipient_email(self):
        payload = {
            "client_id": "your_client_id",
            "client_secret": "your_client_secret",
            "tenant_id": "your_tenant_id",
            "username": "your_username",
            "subject": "Test Subject",
            "body": "Test Body",
            "to_emails": ["invalid-email"]
        }
        response = self.client.post('/send_email', headers={'x-api-key': 'your_api_key'}, json=payload)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
