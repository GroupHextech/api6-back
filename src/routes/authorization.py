# from flask import Blueprint, request, jsonify
# from flask_pymongo import PyMongo
# from ..database import firebase
# from ..database.mongodb import *


# blueprint_auth = Blueprint("auth", __name__, url_prefix="/api")

# @blueprint_auth.route('/authorize', methods=['GET', 'POST'])
# def authorize():
#     if request.method == 'GET':
#         client_id = request.args.get('client_id')
#         client = client.db.clients.get(client_id)
#         if not client:
#             return 'Client not found', 404
#         return f'''
#             <form method="post">
#                 <input type="hidden" name="client_id" value="{client_id}">
#                 <input type="hidden" name="redirect_uri" value="{request.args.get('redirect_uri')}">
#                 <input type="hidden" name="scope" value="{request.args.get('scope')}">
#                 <input type="hidden" name="response_type" value="{request.args.get('response_type')}">
#                 <button type="submit">Authorize</button>
#             </form>
#         '''
#     if request.method == 'POST':
#         client_id = request.form['client_id']
#         redirect_uri = request.form['redirect_uri']
#         scope = request.form['scope']
#         response_type = request.form['response_type']
#         user = firebase.get_user_by_id(session['user_id'])
#         if not user:
#             return redirect('/login')
#         grant_user = user
#         return authorization.create_authorization_response(grant_user=grant_user)

# @blueprint_auth.route('/token', methods=['POST'])
# def issue_token():
#     return authorization.create_token_response()

# @blueprint_auth.route('/revoke', methods=['POST'])
# def revoke_token():
#     return authorization.creat