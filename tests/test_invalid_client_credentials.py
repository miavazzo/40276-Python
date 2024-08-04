# tests/test_invalid_client_credentials.py

import os
import sys
import unittest
import json

# Aggiungi il percorso dell'applicazione alla sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.config import Config

class TestInvalidClientCredentials(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_invalid_client_credentials(self):
        payload = {
            "client_id": "invalid_client_id",
            "client_secret": "invalid_client_secret",
            "tenant_id": "valid_tenant_id",
            "username": "valid_username",
            "subject": "Test Email",
            "body": "This is a test email.",
            "to_emails": ["test@example.com"],
            "attachments": []
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": Config.API_KEY
        }
        response = self.client.post('/send_email', data=json.dumps(payload), headers=headers)
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.data)
        self.assertIn("Impossibile ottenere il token di accesso", response_data["error"])

if __name__ == '__main__':
    unittest.main()
