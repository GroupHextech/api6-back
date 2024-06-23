from authlib.oauth2.rfc6749 import grants
from flask_pymongo import PyMongo
# from ..repositories import user_repository
from datetime import datetime, timedelta
from ..database import firebase
from ..database.mongodb import *

class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    def save_authorization_code(self, code, request):
        item = {
            'code': code,
            'client_id': request.client.client_id,
            'redirect_uri': request.redirect_uri,
            'scope': request.scope,
            'user_id': request.user.get_user_id(),
            'expires_at': datetime.utcnow() + timedelta(minutes=10)
        }
        client.db.authorization_codes.insert_one(item)

    def query_authorization_code(self, code, client):
        return client.db.authorization_codes.find_one({'code': code, 'client_id': client.client_id})

    def delete_authorization_code(self, authorization_code):
        client.db.authorization_codes.delete_one({'code': authorization_code['code']})

    def authenticate_user(self, authorization_code):
        return firebase.get_user_by_id.get(authorization_code['user_id'])