"""
Test per il servizio email.
"""

import os
import sys
import unittest
from unittest.mock import patch
from dotenv import load_dotenv
from app.email_service import get_access_token  # noqa: E402

# Aggiungi il percorso al modulo email_service
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Carica le variabili d'ambiente dal file .env
load_dotenv()

class TestEmailService(unittest.TestCase):
    """Classe per testare il servizio email"""

    @patch(
        'msal.ConfidentialClientApplication.acquire_token_for_client', 
        return_value={"error": "invalid_client"}
    )
    @patch(
        'msal.ConfidentialClientApplication.acquire_token_silent', 
        return_value=None
    )
    def test_get_access_token_failure(self,
            mock_acquire_token_silent,
            mock_acquire_token_for_client
        ):
        """Test ottenimento token di accesso - Fallimento"""
        # Assicuriamoci che le variabili d'ambiente siano impostate
        print(f"TENANT_ID: {os.environ.get('TENANT_ID')}")
        print(f"CLIENT_ID: {os.environ.get('CLIENT_ID')}")
        print(f"CLIENT_SECRET: {os.environ.get('CLIENT_SECRET')}")

        # Eseguiamo la funzione per ottenere il token
        token = get_access_token()
        self.assertIsNone(token)

if __name__ == '__main__':
    unittest.main()
