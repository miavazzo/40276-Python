import unittest
from unittest.mock import patch, MagicMock
import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

import app.email_service as email_service

class TestEmailService(unittest.TestCase):

    @patch('app.email_service.get_access_token', return_value="fake_access_token")
    @patch('app.email_service.requests.post')
    def test_send_email_with_attachments_success(self, mock_post, mock_get_access_token):
        mock_post.return_value.status_code = 202
        mock_post.return_value.json.return_value = {}

        subject = "40276-Test Email"
        body = "This is a test email."
        to_email = "massimiliano.iavazzo@capgemini.com"
        attachments = [
            {"path": r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. 40276 parametri email portale clienti - fatture Newatt\Crypto101.pdf", "filename": "Crypto101.pdf"},
            {"path": r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. 40276 parametri email portale clienti - fatture Newatt\Form-Argon-Design-Form.pdf", "filename": "Form-Argon-Design-Form.pdf"},
            {"path": r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. 40276 parametri email portale clienti - fatture Newatt\test1.docx", "filename": "test1.docx"},
            {"path": r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. 40276 parametri email portale clienti - fatture Newatt\test2.docx", "filename": "test2.docx"},
            {"path": r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. 40276 parametri email portale clienti - fatture Newatt\test3.docx", "filename": "test3.docx"}
        ]

        result = email_service.send_email_with_attachments(subject, body, to_email, attachments)
        print("Debug: Result from test_send_email_with_attachments_success")
        print(result)
        self.assertIsNotNone(result.get("status"))
        self.assertEqual(result.get("status"), "Email inviata con successo!")

    @patch('app.email_service.get_access_token', return_value="fake_access_token")
    @patch('app.email_service.requests.post')
    def test_send_email_with_attachments_failure(self, mock_post, mock_get_access_token):
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {"error": "BadRequest"}

        subject = "40276-Test Email"
        body = "This is a test email."
        to_email = "massimiliano.iavazzo@capgemini.com"
        attachments = [
            {"path": r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. 40276 parametri email portale clienti - fatture Newatt\Crypto101.pdf", "filename": "Crypto101.pdf"},
            {"path": r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. 40276 parametri email portale clienti - fatture Newatt\Form-Argon-Design-Form.pdf", "filename": "Form-Argon-Design-Form.pdf"},
            {"path": r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. 40276 parametri email portale clienti - fatture Newatt\test1.docx", "filename": "test1.docx"},
            {"path": r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. 40276 parametri email portale clienti - fatture Newatt\test2.docx", "filename": "test2.docx"},
            {"path": r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. 40276 parametri email portale clienti - fatture Newatt\test3.docx", "filename": "test3.docx"}
        ]

        result = email_service.send_email_with_attachments(subject, body, to_email, attachments)
        print("Debug: Result from test_send_email_with_attachments_failure")
        print(result)
        self.assertIsNotNone(result.get("status"))
        self.assertIn("Errore nell'invio dell'email", result.get("status"))

    @patch('app.email_service.ConfidentialClientApplication.acquire_token_for_client', return_value={"error": "invalid_client"})
    def test_get_access_token_failure(self, mock_acquire):
        token = email_service.get_access_token()
        self.assertIsNone(token)

if __name__ == '__main__':
    unittest.main()
