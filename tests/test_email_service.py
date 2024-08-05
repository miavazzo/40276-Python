import unittest
import os
import sys

# Aggiungi il percorso dell'applicazione alla sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'tests')))

# Carica tutti i test dai file di test
test_modules = [
    'test_dotenv',
    'test_email_body_formats',
    'test_get_access_token_failure',
    'test_invalid_api_key',
    'test_invalid_attachments',
    'test_invalid_base64_attachment',
    'test_invalid_client_credentials',
    'test_invalid_recipient_email',
    'test_large_attachments',
    'test_large_number_of_attachments',
    'test_missing_api_key',
    'test_missing_parameters',
    'test_multiple_recipients',
    'test_network_error',
    'test_rate_limiting',
    'test_valid_email',
]

suite = unittest.TestSuite()

# Aggiungi i test alla suite
for tm in test_modules:
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(tm))

# Esegui i test
runner = unittest.TextTestRunner()
runner.run(suite)
