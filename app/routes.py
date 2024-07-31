from flask import request, jsonify, current_app
import base64
from .email_service import send_email_with_attachment

@current_app.route('/send_email', methods=['POST'])
def send_email():
    api_key = request.headers.get('x-api-key')
    if api_key != current_app.config['API_KEY']:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    subject = data.get('subject')
    body = data.get('body')
    to_email = data.get('to_email')
    attachment = data.get('attachment', None)

    if attachment:
        attachment_path = "attachment"
        with open(attachment_path, "wb") as f:
            f.write(base64.b64decode(attachment))
    else:
        attachment_path = None

    result = send_email_with_attachment(subject, body, to_email, attachment_path)

    return jsonify(result), 200
