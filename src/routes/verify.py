# src/routes/verify.py
from flask import Blueprint, request, jsonify
import pyotp
from ..repositories.user_secrets import get_user_secret

bp_verify = Blueprint('verify', __name__)

@bp_verify.route('/verify', methods=['POST'])
def verify():
    data = request.json
    email = data['email']
    token = data['token']
    secret = get_user_secret(email)

    if not secret:
        return jsonify({'message': 'No secret found for this user'}), 400

    totp = pyotp.TOTP(secret)
    verified = totp.verify(token)

    if verified:
        return jsonify({'message': 'Verified'})
    else:
        return jsonify({'message': 'Invalid token'}), 400
