import unittest
import json
import os
import sys

# Aggiungi il percorso dell'applicazione alla sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.config import Config

class TestMissingParameters(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.api_key = Config.API_KEY  # Prendi la chiave API dalla configurazione

    def test_missing_parameters(self):
        headers = {'x-api-key': self.api_key, 'Content-Type': 'application/json'}
        response = self.client.post('/send_email', headers=headers, data=json.dumps({}))
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
