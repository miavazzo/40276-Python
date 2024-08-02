"""
Unit tests for the email_service module.

This module contains tests for the send_email_with_attachments function 
in the email_service module. It uses the unittest framework and mocks 
external dependencies to test the functionality.

Environment Variables:
    The environment variables are loaded from a .env file using the 
    load_dotenv function from the dotenv package.

Classes:
    TestEmailService: Contains unit tests for the email_service module.

Functions:
    test_send_email_with_attachments_success(self, mock_post): 
        Tests the successful sending of an email with attachments.
"""
import unittest
import os
from unittest.mock import patch
from dotenv import load_dotenv
import app.email_service as email_service
# import os is not used, so it can be safely removed

# Carica le variabili d'ambiente dal file .env
load_dotenv()
class TestEmailService(unittest.TestCase):
    """
    Unit tests for the email_service module.

    This class contains unit tests for the send_email_with_attachments function 
    in the email_service module. It uses the unittest framework and mocks 
    external dependencies to test the functionality.

    Methods:
        setUp(self): Sets up the test environment by loading environment variables.
        test_send_email_with_attachments_success(self, mock_post): 
            Tests the successful sending of an email with attachments.
    """
    @patch('app.email_service.get_access_token', return_value="fake_access_token")
    @patch('app.email_service.requests.post')
    def test_send_email_with_attachments_success(self, mock_post, mock_get_access_token):
        """
        Sets up the test environment by loading environment variables.

        This method is called before each test case. It ensures that the necessary 
        environment variables are loaded from the .env file to simulate the 
        application's environment.
        """
        mock_post.return_value.status_code = 202
        mock_post.return_value.json.return_value = {}

        subject = "40240-Test Email"
        body = "This is a test email."
        to_email = "massimiliano.iavazzo@capgemini.com"
        attachments = [
            {
                "path": (
                    r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T"
                    r". 40240 parametri email portale clienti - "
                    r"fatture Newatt\Crypto101.pdf"
                ),
                "filename": "Crypto101.pdf"
            },
            {
                "path": (
                    r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T." 
                    r" 40240 parametri email portale clienti - "
                    r"fatture Newatt\Form-Argon-Design-Form.pdf"
                ),
                "filename": "Form-Argon-Design-Form.pdf"
            },
            {
                "path": (
                    r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T." 
                    r" 40240 parametri email portale clienti - "
                    r"fatture Newatt\test1.docx"
                ),
                "filename": "test1.docx"
            },
            {
                "path": (
                    r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. "
                    r"40240 parametri email portale clienti - "
                    r"fatture Newatt\test2.docx"
                ),
                "filename": "test2.docx"
            },
            {
                "path": (
                    r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. "
                    r"40240 parametri email portale clienti - "
                    r"fatture Newatt\test3.docx"
                ),
                "filename": "test3.docx"
            }
        ]

        result = email_service.send_email_with_attachments(subject, body, to_email, attachments)
        print("Debug: Result from test_send_email_with_attachments_success")
        print(result)
        self.assertIsNotNone(result.get("status"))
        self.assertEqual(result.get("status"), "Email inviata con successo!")

    @patch('app.email_service.get_access_token', return_value="fake_access_token")
    @patch('app.email_service.requests.post')
    def test_send_email_with_attachments_failure(self, mock_post, mock_get_access_token):
        """
        Tests the successful sending of an email with attachments.

        This test mocks the requests.post method and the get_access_token function 
        to simulate sending an email with attachments using the send_email_with_attachments 
        function. It verifies that the function returns the expected status code and response.

        Args:
            mock_post (unittest.mock.Mock): Mock object for the requests.post method.
        """
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {"error": "BadRequest"}

        subject = "40240-Test Email"
        body = "This is a test email."
        to_email = "massimiliano.iavazzo@capgemini.com"
        attachments = [
            {
                "path": (
                    r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T"
                    r". 40240 parametri email portale clienti - "
                    r"fatture Newatt\Crypto101.pdf"
                ),
                "filename": "Crypto101.pdf"
            },
            {
                "path": (
                    r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. "
                    r"40240 parametri email portale clienti - "
                    r"fatture Newatt\Form-Argon-Design-Form.pdf"
                ),
                "filename": "Form-Argon-Design-Form.pdf"
            },
            {
                "path": (
                    r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. "
                    r"40240 parametri email portale clienti - "
                    r"fatture Newatt\test1.docx"
                ),
                "filename": "test1.docx"
            },
            {
                "path": (
                    r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. "
                    r"40240 parametri email portale clienti - "
                    r"fatture Newatt\test2.docx"
                ),
                "filename": "test2.docx"
            },
            {
                "path": (
                    r"C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. "
                    r"40240 parametri email portale clienti - "
                    r"fatture Newatt\test3.docx"
                ),
                "filename": "test3.docx"
            }
        ]

        result = email_service.send_email_with_attachments(subject, body, to_email, attachments)
        print("Debug: Result from test_send_email_with_attachments_failure")
        print(result)
        self.assertIsNotNone(result.get("status"))
        self.assertIn("Errore nell'invio dell'email", result.get("status"))

    @patch(
        'app.email_service.ConfidentialClientApplication.acquire_token_for_client', 
        return_value={"error": "invalid_client"}
    )
    def test_get_access_token_failure(self, mock_acquire_token):
        """
        Tests the failure scenario when retrieving an access token.

        This test mocks the acquire_token_for_client method to simulate a failure 
        when retrieving an access token using the get_access_token function. 
        It verifies that the function handles the error correctly and returns None.

        Args:
            mock_acquire_token (unittest.mock.Mock): Mock object for the 
            acquire_token_for_client method.
        """
        # Mock the authority variable
        with patch(
            'app.email_service.authority', 
            new=f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}"
            ):
            token = email_service.get_access_token()
            self.assertIsNone(token)

if __name__ == '__main__':
    unittest.main()
