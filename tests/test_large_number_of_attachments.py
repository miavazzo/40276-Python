import unittest
import os
import sys
import base64
from flask import json
from dotenv import load_dotenv

# Aggiungi il percorso dell'applicazione alla sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.config import Config

class TestLargeNumberOfAttachments(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        load_dotenv()
        self.api_key = Config.API_KEY
        assert self.api_key is not None, "API key non trovata"

    def test_large_number_of_attachments(self):
        # Prepara i dati di test prendendoli da Config
        attachments = []
        for i in range(100):
            attachment_content = base64.b64encode(os.urandom(1024)).decode('utf-8')  # 1 KB per ogni allegato
            attachments.append({"content": attachment_content, "filename": f"attachment_{i}.txt"})

        data = {
            "client_id": Config.CLIENT_ID,
            "client_secret": Config.CLIENT_SECRET,
            "tenant_id": Config.TENANT_ID,
            "username": Config.USERNAME,
            "subject": "Test Subject",
            "body": "Test Body",
            "to_emails": ["valid@example.com"],
            "attachments": attachments
        }

        # Effettua la richiesta
        response = self.client.post('/send_email', data=json.dumps(data), content_type='application/json', headers={"x-api-key": self.api_key})

        # Stampa di debug
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.data.decode('utf-8')}")

        # Verifica che la risposta sia 202 Accepted
        self.assertEqual(response.status_code, 202)

if __name__ == '__main__':
    unittest.main()
