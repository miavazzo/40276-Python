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
import requests
from msal import ConfidentialClientApplication

def get_access_token(client_id, client_secret, tenant_id):
    authority = f'https://login.microsoftonline.com/{tenant_id}'
    app = ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret  # Assicurati che client_secret sia una stringa e non un dizionario
    )
    result = app.acquire_token_silent(scopes=['https://graph.microsoft.com/.default'], account=None)
    if not result:
        result = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])

    if "access_token" in result:
        return result['access_token'], None
    else:
        return None, result.get("error_description")

def send_email_with_attachments(client_id, client_secret, tenant_id, username, subject, body, to_emails, attachments=None):
    access_token, error_description = get_access_token(client_id, client_secret, tenant_id)
    if not access_token:
        return {"error": f"Impossibile ottenere il token di accesso: {error_description}"}, 500

    endpoint = f'https://graph.microsoft.com/v1.0/users/{username}/sendMail'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }

    email_msg = {
        'message': {
            'subject': subject,
            'body': {
                'contentType': 'Text',
                'content': body
            },
            'toRecipients': [{'emailAddress': {'address': email}} for email in to_emails],
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
