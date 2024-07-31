import unittest
from unittest.mock import patch, MagicMock
import app.email_service as email_service

class TestEmailService(unittest.TestCase):

    @patch('app.email_service.requests.post')
    def test_send_email_with_attachments_success(self, mock_post):
        mock_post.return_value.status_code = 202
        mock_post.return_value.json.return_value = {}

        subject = "Test Email"
        body = "This is a test email."
        to_email = "test@example.com"
        attachments = [{"path": "testfile.txt", "filename": "testfile.txt"}]

        result = email_service.send_email_with_attachments(subject, body, to_email, attachments)
        self.assertEqual(result["status"], "Email inviata con successo!")

    @patch('app.email_service.requests.post')
    def test_send_email_with_attachments_failure(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {"error": "BadRequest"}

        subject = "Test Email"
        body = "This is a test email."
        to_email = "test@example.com"
        attachments = [{"path": "testfile.txt", "filename": "testfile.txt"}]

        result = email_service.send_email_with_attachments(subject, body, to_email, attachments)
        self.assertIn("Errore nell'invio dell'email.", result["status"])

    def test_get_access_token_failure(self):
        with patch('app.email_service.ConfidentialClientApplication.acquire_token_for_client', return_value={"error": "invalid_client"}) as mock_acquire:
            token = email_service.get_access_token()
            self.assertIsNone(token[0])
            self.assertEqual(token[1]['error'], "invalid_client")

if __name__ == '__main__':
    unittest.main()
