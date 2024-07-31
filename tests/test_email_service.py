# tests/test_email_service.py

import unittest
from app.email_service import send_email_with_attachment

class TestEmailService(unittest.TestCase):
    def test_send_email_without_attachment(self):
        result = send_email_with_attachment("Test Subject", "Test Body", "test@example.com")
        self.assertIn("status", result)
        self.assertIn("request", result)
        self.assertIn("response", result)
    
    def test_send_email_with_attachment(self):
        # Assicurati che il file di test esista
        attachment_path = "tests/testfile.txt"
        with open(attachment_path, "w") as f:
            f.write("This is a test file.")
        result = send_email_with_attachment("Test Subject", "Test Body", "test@example.com", attachment_path)
        self.assertIn("status", result)
        self.assertIn("request", result)
        self.assertIn("response", result)

if __name__ == '__main__':
    unittest.main()
