import unittest
import json
import os
import sys

# Aggiungi il percorso dell'applicazione alla sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.config import Config  # Assumendo che Config.py sia in app

class TestInvalidAPIKey(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_invalid_api_key(self):
        headers = {'x-api-key': 'invalid_api_key', 'Content-Type': 'application/json'}
        payload = {
            "subject": "Test Email",
            "body": "This is a test email.",
            "to_emails": ["test@example.com"]
        }
        response = self.client.post('/send_email', headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
