import unittest
import json
import os
import sys
from unittest.mock import patch
import base64
import jwt  # Assicurati di avere il pacchetto PyJWT installato

# Aggiungi il percorso dell'applicazione alla sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.config import Config

class TestInvalidRecipientEmail(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        self.api_key = Config.API_KEY  # Carica l'API_KEY dal file .env

        self.valid_payload = {
            "client_id": "valid_client_id",
            "client_secret": "valid_client_secret",
            "tenant_id": "valid_tenant_id",
            "username": "valid_username",
            "subject": "Test Subject",
            "body": "Test Body",
            "to_emails": ["invalid_email_format"]
        }

    @patch('app.email_service.get_access_token')
    def test_invalid_recipient_email(self, mock_get_access_token):
        # Genera un token JWT ben formato
        mock_token = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')
        mock_get_access_token.return_value = (mock_token, None)

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
        response = self.client.post('/send_email', data=json.dumps(self.valid_payload), headers=headers)
        print("Response data:", response.get_data(as_text=True))
        print("Response status code:", response.status_code)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid recipient email format', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
