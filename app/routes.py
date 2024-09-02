# app/routes.py
"""
    routing module per l'API con utilizzo di logging
"""

import base64
import os
import logging
from flask import request, jsonify, Blueprint, current_app
from .email_service import send_email_with_attachments

# Configurazione del logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='api_debug.log',
                    filemode='a')

bp = Blueprint('email', __name__)

@bp.route('/send_email', methods=['POST'])
def send_email():
    '''
    rotta per l'invio di email con allegati. 
    richiede un API key per l'autenticazione.
    '''
    logging.info("Received request to /send_email")

    # Log headers (escludendo l'API key per sicurezza)
    headers = dict(request.headers)
    if 'x-api-key' in headers:
        headers['x-api-key'] = '[REDACTED]'
    logging.debug(f"Request Headers: {headers}")

    api_key = request.headers.get('x-api-key')
    if api_key != current_app.config['API_KEY']:
        logging.warning("Unauthorized access attempt")
        return jsonify({"error": "Unauthorized"}), 401

    logging.info("API key authentication successful")

    try:
        data = request.json
        logging.debug(f"Received JSON data: {data}")
    except Exception as e:
        logging.error(f"Error parsing JSON: {str(e)}")
        return jsonify({"error": "Invalid JSON format"}), 400

    required_fields = ['client_id',
                       'client_secret',
                       'tenant_id',
                       'username',
                       'subject',
                       'body',
                       'to_emails']
    for field in required_fields:
        if field not in data or not data[field]:
            logging.error(f"Missing required field: {field}")
            return jsonify({"error": f"Missing required parameter: {field}"}), 400

    client_id = data.get('client_id')
    client_secret = data.get('client_secret')
    tenant_id = data.get('tenant_id')
    username = data.get('username')
    subject = data.get('subject')
    body = data.get('body')
    to_emails = data.get('to_emails')
    cc_emails = data.get('cc_emails', [])
    bcc_emails = data.get('bcc_emails', [])
    attachments = data.get('attachments', [])
    is_html = data.get('is_html', False)

    logging.info("All required fields are present")
    logging.debug(f"client_id: {client_id}")
    logging.debug(f"tenant_id: {tenant_id}")
    logging.debug(f"username: {username}")
    logging.debug(f"subject: {subject}")
    logging.debug(f"to_emails: {to_emails}")
    logging.debug(f"cc_emails: {cc_emails}")
    logging.debug(f"bcc_emails: {bcc_emails}")
    logging.debug(f"is_html: {is_html}")
    logging.debug(f"Number of attachments: {len(attachments)}")

    saved_attachments = []
    for i, attachment in enumerate(attachments):
        attachment_path = f"attachment_{i}"
        try:
            with open(attachment_path, "wb") as f:
                f.write(base64.b64decode(attachment['content']))
            saved_attachments.append({"path": attachment_path, "filename": attachment.get('filename')})
            logging.debug(f"Attachment saved: {attachment.get('filename')}")
        except Exception as e:
            logging.error(f"Error saving attachment {i}: {str(e)}")

    logging.info("Calling send_email_with_attachments function")
    result, status_code = send_email_with_attachments(
        client_id, client_secret, tenant_id, username, subject,
        body, to_emails, cc_emails, bcc_emails, saved_attachments,
        is_html
    )

    for attachment in saved_attachments:
        try:
            os.remove(attachment["path"])
            logging.debug(f"Temporary file removed: {attachment['path']}")
        except Exception as e:
            logging.error(f"Error removing temporary file {attachment['path']}: {str(e)}")

    logging.info(f"Email sending attempt completed with status code: {status_code}")
    logging.debug(f"Email sending result: {result}")

    return jsonify(result), status_code

# Aggiungo l'endpoint di ping
@bp.route('/ping', methods=['GET'])
def ping():
    '''
    rotta per verificare se l'API è raggiungibile
    '''
    logging.info("Received request to /ping")
    return jsonify({"message": "API is reachable"}), 200