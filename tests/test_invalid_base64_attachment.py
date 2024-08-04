import unittest
import json
import os
import sys

# Aggiungi il percorso dell'applicazione alla sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.config import Config

class TestInvalidBase64Attachment(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_invalid_base64_attachment(self):
        headers = {'x-api-key': os.getenv('APP_API_KEY'), 'Content-Type': 'application/json'}
        payload = {
            "subject": "Test Email",
            "body": "This is a test email.",
            "to_emails": ["test@example.com"],
            "attachments": [
                {
                    "filename": "test.txt",
                    "content": "invalid_base64"
                }
            ]
        }
        response = self.client.post('/send_email', headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
