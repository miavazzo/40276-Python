import unittest
import os
import sys
from flask import json
from dotenv import load_dotenv

# Aggiungi il percorso dell'applicazione alla sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.config import Config

class TestInvalidAttachments(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        load_dotenv()
        self.api_key = Config.API_KEY
        assert self.api_key is not None, "API key non trovata"

    def test_invalid_attachments(self):
        # Prepara i dati di test prendendoli da Config
        data = {
            "client_id": Config.CLIENT_ID,
            "client_secret": Config.CLIENT_SECRET,
            "tenant_id": Config.TENANT_ID,
            "username": Config.USERNAME,
            "subject": "Test Subject",
            "body": "Test Body",
            "to_emails": ["valid@example.com"],
            "attachments": [{"path": "nonexistent_file.txt"}]
        }

        # Effettua la richiesta
        response = self.client.post('/send_email', data=json.dumps(data), content_type='application/json', headers={"x-api-key": self.api_key})

        # Stampa di debug
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.data.decode('utf-8')}")

        # Verifica che la risposta sia 500 Internal Server Error
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()