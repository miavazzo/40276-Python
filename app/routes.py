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
BASE_DIR = r"E:\progetti\email_api_oauth2"
LOG_FILE = os.path.join(BASE_DIR, 'api_debug.log')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=LOG_FILE,
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
    logging.debug("Request Headers: %s", headers)

    api_key = request.headers.get('x-api-key')
    expected_api_key = current_app.config['API_KEY']
    logging.debug(f"Received API key: {api_key[:4]}..." if api_key else "No API key received")
    logging.debug(f"Expected API key: {expected_api_key[:4]}..." if expected_api_key else "No expected API key found in config")

    if api_key != expected_api_key:
        logging.warning("Unauthorized access attempt")
        return jsonify({"error": "Unauthorized"}), 401

    logging.info("API key authentication successful")

    try:
        data = request.json
        logging.debug("Received JSON data: %s", data)
    except Exception as e:
        logging.error("Error parsing JSON: %s", str(e))
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
            logging.error("Missing required field: %s", field)
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
    logging.debug("client_id: %s", client_id)
    logging.debug("tenant_id: %s", tenant_id)
    logging.debug("username: %s", username)
    logging.debug("subject: %s", subject)
    logging.debug("to_emails: %s", to_emails)
    logging.debug("cc_emails: %s", cc_emails)
    logging.debug("bcc_emails: %s", bcc_emails)
    logging.debug("is_html: %s", is_html)
    logging.debug("Number of attachments: %s", len(attachments))

    saved_attachments = []
    for i, attachment in enumerate(attachments):
        attachment_path = os.path.join(BASE_DIR, f"attachment_{i}")
        try:
            with open(attachment_path, "wb") as f:
                f.write(base64.b64decode(attachment['content']))
            saved_attachments.append({"path": attachment_path,
                                      "filename": attachment.get('filename')})
            logging.debug("Attachment saved: %s", attachment.get('filename'))
        except Exception as e:
            logging.error("Error saving attachment %s: %s", i, str(e))

    logging.info("Calling send_email_with_attachments function")
    result, status_code = send_email_with_attachments(
        client_id, client_secret, tenant_id, username, subject,
        body, to_emails, cc_emails, bcc_emails, saved_attachments,
        is_html
    )

    for attachment in saved_attachments:
        try:
            os.remove(attachment["path"])
            logging.debug("Temporary file removed: %s", attachment["path"])
        except Exception as e:
            logging.error("Error removing temporary file %s: %s", attachment["path"], str(e))

    logging.info("Email sending attempt completed with status code: %s", status_code)
    logging.debug("Email sending result: %s", result)

    return jsonify(result), status_code

@bp.route('/ping', methods=['GET'])
def ping():
    '''
    rotta per verificare se l'API è raggiungibile
    '''
    client_ip = request.remote_addr
    logging.info("Received request to /ping from %s", client_ip)
    return jsonify({"message": "API is reachable"}), 200
