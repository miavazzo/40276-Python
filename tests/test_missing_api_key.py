import unittest
import os
import sys

# Aggiungi il percorso dell'applicazione alla sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import json
from app import create_app

class TestMissingApiKey(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_missing_api_key(self):
        # Prepara i dati di test
        data = {
            "client_id": "valid_client_id",
            "client_secret": "valid_client_secret",
            "tenant_id": "valid_tenant_id",
            "username": "valid_username",
            "subject": "Test Subject",
            "body": "Test Body",
            "to_emails": ["valid@example.com"]
        }

        # Effettua la richiesta senza la chiave API
        response = self.client.post('/send_email', data=json.dumps(data), content_type='application/json')
        
        # Verifica che la risposta sia 401 Unauthorized
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
