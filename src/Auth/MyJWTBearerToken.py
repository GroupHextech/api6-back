import jwt
from datetime import datetime, timedelta
from flask_pymongo import PyMongo
from authlib.oauth2.rfc9068 import JWTBearerTokenGenerator
from flask import current_app
from ..database.mongodb import *

class MyJWTBearerToken(JWTBearerTokenGenerator):
    def __init__(self, algorithm='HS256'):
        self.secret_key = current_app.config['SECRET_KEY'] # secret_key
        self.algorithm = algorithm

    def create_token(self, client, grant_type, user=None, scope=None, expires_in=None, include_refresh_token=True):
        payload = {
            'iss': 'your-issuer',
            'aud': client.client_id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in or 3600),
            'iat': datetime.utcnow(),
            'scope': scope,
            'sub': user.get_user_id() if user else None
        }
        access_token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        token = {
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': expires_in or 3600,
            'scope': scope
        }
        if include_refresh_token:
            refresh_payload = payload.copy()
            refresh_payload['exp'] = datetime.utcnow() + timedelta(days=30)
            token['refresh_token'] = jwt.encode(refresh_payload, self.secret_key, algorithm=self.algorithm)

        self.save_token(token, client, user)
        return token

    def save_token(self, token, client, user):
        item = token.copy()
        item.update({
            'client_id': client.client_id,
            'user_id': user.get_user_id() if user else None,
            'issued_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(seconds=token['expires_in'])
        })
        client.db.tokens.insert_one(item)
