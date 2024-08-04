# tests/test_large_attachments.py

import os
import sys
import unittest
import json
import base64

# Aggiungi il percorso dell'applicazione alla sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.config import Config

class TestLargeAttachments(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_large_attachments(self):
        # Simula un allegato grande
        large_content = base64.b64encode(os.urandom(10 * 1024 * 1024)).decode('utf-8')  # 10 MB
        payload = {
            "client_id": Config.CLIENT_ID,
            "client_secret": Config.CLIENT_SECRET,
            "tenant_id": Config.TENANT_ID,
            "username": Config.USERNAME,
            "subject": "Test Email with Large Attachments",
            "body": "This is a test email with a large attachment.",
            "to_emails": ["test@example.com"],
            "attachments": [
                {
                    "filename": "large_file.txt",
                    "content": large_content
                }
            ]
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": Config.API_KEY
        }
        response = self.client.post('/send_email', data=json.dumps(payload), headers=headers)
        self.assertEqual(response.status_code, 202)
        response_data = json.loads(response.data)
        self.assertIn("Email inviata con successo!", response_data["status"])

if __name__ == '__main__':
    unittest.main()
