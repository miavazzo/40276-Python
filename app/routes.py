'''
file di smistaggio delle richieste in ingresso alle varie rotte dell'API
'''
# app/routes.py

import base64
import os
from flask import request, jsonify, Blueprint, current_app
from .email_service import send_email_with_attachments

bp = Blueprint('email', __name__)

@bp.route('/send_email', methods=['POST'])
def send_email():
    '''
    rotta per l'invio di email con allegati. 
    richiede un API key per l'autenticazione.
    '''
    api_key = request.headers.get('x-api-key')
    if api_key != current_app.config['API_KEY']:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
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

    if not all([client_id, client_secret, tenant_id, username, subject, body, to_emails]):
        return jsonify({"error": "Missing required parameters"}), 400

    saved_attachments = []
    for attachment in attachments:
        attachment_path = f"attachment_{attachments.index(attachment)}"
        with open(attachment_path, "wb") as f:
            f.write(base64.b64decode(attachment['content']))
        saved_attachments.append({"path": attachment_path, "filename": attachment.get('filename')})

    result, status_code = send_email_with_attachments(
        client_id, client_secret, tenant_id, username, subject, 
        body, to_emails, cc_emails, bcc_emails, saved_attachments, 
        is_html
    )

    for attachment in saved_attachments:
        os.remove(attachment["path"])

    return jsonify(result), status_code
