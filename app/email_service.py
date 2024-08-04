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
import requests
import base64
import mimetypes
from msal import ConfidentialClientApplication

def get_access_token(client_id, client_secret, tenant_id):
    authority = f'https://login.microsoftonline.com/{tenant_id}'
    scopes = ['https://graph.microsoft.com/.default']

    app = ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential={"client_secret": client_secret}
    )
    result = app.acquire_token_silent(scopes, account=None)
    if not result:
        result = app.acquire_token_for_client(scopes=scopes)

    if "access_token" in result:
        return result['access_token'], None
    else:
        return None, result.get('error_description', 'Unknown error')

def send_email_with_attachments(client_id, client_secret, tenant_id, username, subject, body, to_emails, attachments=None):
    access_token, error_description = get_access_token(client_id, client_secret, tenant_id)
    if not access_token:
        return {"error": "Unauthorized", "description": error_description}, 401

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

    for email in to_emails:
        if '@' not in email:
            return {"error": "Invalid recipient email"}, 400

    if attachments:
        for attachment in attachments:
            try:
                with open(attachment['path'], 'rb') as file:
                    attachment_content = base64.b64encode(file.read()).decode('utf-8')
            except (FileNotFoundError, IOError) as e:
                return {"error": f"Error reading file {attachment['path']}: {str(e)}"}, 400
            except base64.binascii.Error:
                return {"error": "Invalid base64 attachment"}, 400

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

    try:
        response = requests.post(endpoint, headers=headers, json=email_msg, timeout=10)
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}, 500

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

    return result, response.status_code