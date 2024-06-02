from flask import Blueprint, request, jsonify
import pyotp
import qrcode
from io import BytesIO
import base64
from ..repositories.user_secrets import save_user_secret

bp_generate = Blueprint('generate', __name__)

@bp_generate.route('/generate', methods=['POST'])
def generate():
    data = request.json
    email = data['email']
    secret = pyotp.random_base32()
    save_user_secret(email, secret)
    
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(name=email, issuer_name='HexAnalytics')

    # Gerar o QR Code
    qr = qrcode.make(provisioning_uri)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    qr_code_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return jsonify({'secret': secret, 'qrcode': f'data:image/png;base64,{qr_code_image}'})
