import os
import requests
import base64
import mimetypes
from msal import ConfidentialClientApplication

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
tenant_id = os.environ.get('TENANT_ID')
authority = f'https://login.microsoftonline.com/{tenant_id}'
scopes = ['https://graph.microsoftonline.com/.default']
username = os.environ.get('APP_USERNAME')
API_KEY = os.environ.get('API_KEY')

def get_access_token():
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
        return None, result

def send_email_with_attachments(subject, body, to_email, attachments=None):
    access_token = get_access_token()
    if not access_token:
        return {"error": "Impossibile ottenere il token di accesso."}

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
            'toRecipients': [
                {
                    'emailAddress': {
                        'address': to_email
                    }
                }
            ],
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

    print("Request:")
    print(f"URL: {endpoint}")
    print(f"Headers: {headers}")
    print(f"Email Message: {email_msg}")

    response = requests.post(endpoint, headers=headers, json=email_msg)

    print("Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Body: {response.text}")

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

    return result
