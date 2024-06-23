# from authlib.oauth2.rfc6749.tokens import BearerToken
# from werkzeug.security import gen_salt
# from datetime import datetime, timedelta

# class MyBearerToken(BearerToken):
#     def create_token(self, client, grant_type, user=None, scope=None, expires_in=None, include_refresh_token=True):
#         token = {
#             'access_token': self.generate_token(),
#             'token_type': 'Bearer',
#             'expires_in': expires_in or 3600,
#             'scope': scope,
#             'created_at': datetime.utcnow()
#         }
#         if include_refresh_token:
#             token['refresh_token'] = self.generate_token()

#         self.save_token(token, client, user)
#         return token

#     def save_token(self, token, client, user):
#         item = token.copy()
#         item.update({
#             'client_id': client.client_id,
#             'user_id': user.get_user_id(),
#             'issued_at': datetime.utcnow(),
#             'expires_at': datetime.utcnow() + timedelta(seconds=token['expires_in'])
#         })
#         client.db.tokens.save(item)
