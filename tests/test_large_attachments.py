import unittest
import json
import base64
from app import create_app

class TestLargeAttachments(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_large_attachments(self):
        large_content = base64.b64encode(b'a' * 10**7).decode('utf-8')  # 10 MB file
        payload = {
            "client_id": "your_client_id",
            "client_secret": "your_client_secret",
            "tenant_id": "your_tenant_id",
            "username": "your_username",
            "subject": "Test Subject",
            "body": "Test Body",
            "to_emails": ["test@example.com"],
            "attachments": [{
                "filename": "test.txt",
                "content": large_content
            }]
        }
        response = self.client.post('/send_email', headers={'x-api-key': 'your_api_key'}, json=payload)
        self.assertEqual(response.status_code, 202)

if __name__ == '__main__':
    unittest.main()
