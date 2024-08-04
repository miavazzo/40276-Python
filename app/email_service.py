"""
This module provides functionality to send emails with optional attachments 
using the Microsoft Graph API.

Environment Variables:
    CLIENT_ID (str): The client ID for the Microsoft application.
    CLIENT_SECRET (str): The client secret for the Microsoft application.
    TENANT_ID (str): The tenant ID for the Microsoft application.
    APP_USERNAME (str): The username for the application.
    API_KEY (str): The API key for the application.

Functions:
    get_access_token(): Retrieves an access token from Microsoft Identity platform.
"""
import os
import mimetypes
import base64
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

"""
client_id = os.getenv('CLIENT_ID') #os.environ.get('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET') #os.environ.get('CLIENT_SECRET')
tenant_id = os.getenv('TENANT_ID') #os.environ.get('TENANT_ID')
authority = f'https://login.microsoftonline.com/{tenant_id}'
scopes = ['https://graph.microsoft.com/.default']
username = os.getenv('APP_USERNAME') #os.environ.get('APP_USERNAME')
API_KEY = os.getenv('APP_API_KEY') #os.environ.get('API_KEY')
"""

def get_access_token(client_id, client_secret, tenant_id):
    """
    Retrieves an access token from the Microsoft Identity platform.

    This function uses the client credentials flow to obtain an access token
    for the Microsoft Graph API. It requires the CLIENT_ID, CLIENT_SECRET, 
    and TENANT_ID passed by input parameters.

    Returns:
        str: The access token required for authenticating API requests.
    """
    authority = f'https://login.microsoftonline.com/{tenant_id}'
    scopes = ['https://graph.microsoft.com/.default']
    app = ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret
    )
    result = app.acquire_token_silent(scopes, account=None)
    if not result:
        result = app.acquire_token_for_client(scopes=scopes)

    if "access_token" in result:
        return result['access_token']
    else:
        return None

def send_email_with_attachments(client_id, client_secret, tenant_id, username, subject, body, to_emails, attachments=None):
    """
    Sends an email with optional attachments using Microsoft Graph API.

    Args:
        client_id (str): The client ID for the Microsoft application.
        client_secret (str): The client secret for the Microsoft application.
        tenant_id (str): The tenant ID for the Microsoft application.
        username (str): The username for the application.
        subject (str): The subject of the email.
        body (str): The body content of the email.
        to_emails (str): The recipient's email address.
        attachments (list, optional): A list of file paths to attach to the email. Defaults to None.

    Returns:
        dict: A dictionary containing the result of the email sending operation. 
              If an error occurs, it contains an error message.
    """
    access_token = get_access_token(client_id, client_secret, tenant_id)    
    if not access_token:
        print("Debug: Impossibile ottenere il token di accesso.")
        return {"error": "Impossibile ottenere il token di accesso."}

    endpoint = f'https://graph.microsoft.com/v1.0/users/{username}/sendMail'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }

    to_recipients = [{"emailAddress": {"address": email}} for email in to_emails]

    email_msg = {
        'message': {
            'subject': subject,
            'body': {
                'contentType': 'Text',
                'content': body
            },
            'toRecipients': to_recipients,
            'attachments': []
        },
        'saveToSentItems': 'true'
    }

    if attachments:
        for attachment in attachments:
            with open(attachment['path'], 'rb') as file:
                attachment_content = base64.b64encode(file.read()).decode('utf-8')
            attachment_name = attachment.get('filename', os.path.basename(attachment['path']))
            content_type, _ = mimetypes.guess_type(attachment['path'])
            if not content_type:
                content_type = 'application/octet-stream'
            email_msg['message']['attachments'].append({
                '@odata.type': '#microsoft.graph.fileAttachment',
                'name': attachment_name,
                'contentType': content_type,
                'contentBytes': attachment_content
            })

    print("Debug: Sending email with the following message:")
    print(email_msg)

    response = requests.post(endpoint, headers=headers, json=email_msg, timeout=10)

    print("Debug: Received response:")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

    result = {
        "request": {
            "method": "POST",
            "url": endpoint,
            "headers": headers,
            "body": "[CONTENUTO OMESSO PER BREVITÀ]"
        },
        "response": {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.text
        }
    }

    if response.status_code == 202:
        result["status"] = "Email inviata con successo!"
    else:
        result["status"] = f"Errore nell'invio dell'email. Codice di stato: {response.status_code}"

    print("Debug: Result after sending email:")
    print(result)

    return result
