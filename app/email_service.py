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
import base64
import os
import mimetypes
from msal import ConfidentialClientApplication
import requests
import re

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def get_access_token(client_id, client_secret, tenant_id):
    try:
        authority = f'https://login.microsoftonline.com/{tenant_id}'
        app = ConfidentialClientApplication(
            client_id,
            authority=authority,
            client_credential=client_secret
        )
        result = app.acquire_token_silent(scopes=['https://graph.microsoft.com/.default'], account=None)
        if not result:
            result = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])

        if "access_token" in result:
            return result['access_token'], None
        else:
            return None, result.get("error_description", "Unknown error")
    except Exception as e:
        return None, str(e)

def send_email_with_attachments(client_id, client_secret, tenant_id, username, subject, body, to_emails, cc_emails, bcc_emails, attachments=None, is_html=False):
    access_token, error_description = get_access_token(client_id, client_secret, tenant_id)
    if not access_token:
        return {"error": f"Impossibile ottenere il token di accesso: {error_description}"}, 401

    for email in to_emails:
        if not is_valid_email(email):
            return {"error": "Invalid recipient email format"}, 400

    endpoint = f'https://graph.microsoft.com/v1.0/users/{username}/sendMail'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }

    content_type = 'HTML' if is_html else 'Text'

    email_msg = {
        'message': {
            'subject': subject,
            'body': {
                'contentType': content_type,
                'content': body
            },
            'toRecipients': [{'emailAddress': {'address': email}} for email in to_emails],
            'ccRecipients': [{'emailAddress': {'address': email}} for email in cc_emails] if cc_emails else [],
            'bccRecipients': [{'emailAddress': {'address': email}} for email in bcc_emails] if bcc_emails else [],
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

    response = requests.post(endpoint, headers=headers, json=email_msg)
    if response.status_code == 202:
        return {"status": "Email inviata con successo!"}, 202
    else:
        return {"error": f"Errore nell'invio dell'email. Codice di stato: {response.status_code}", "response": response.json()}, response.status_code