from flask import request, jsonify, current_app
import base64
import os
from .email_service import send_email_with_attachments

@current_app.route('/send_email', methods=['POST'])
def send_email():
    api_key = request.headers.get('x-api-key')
    if api_key != current_app.config['API_KEY']:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    subject = data.get('subject')
    body = data.get('body')
    to_email = data.get('to_email')
    attachments = data.get('attachments', [])

    # Salva temporaneamente gli allegati
    saved_attachments = []
    for attachment in attachments:
        attachment_path = f"attachment_{attachments.index(attachment)}"
        with open(attachment_path, "wb") as f:
            f.write(base64.b64decode(attachment['content']))
        saved_attachments.append({"path": attachment_path})

    result = send_email_with_attachments(subject, body, to_email, saved_attachments)

    # Rimuovi i file temporanei
    for attachment in saved_attachments:
        os.remove(attachment["path"])

    return jsonify(result), 200
