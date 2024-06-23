from flask import Blueprint, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import gen_salt
from ..database.mongodb import *

blueprint_clients = Blueprint("clients", __name__, url_prefix="/api")

@blueprint_clients.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        client_id = gen_salt(24)
        client_secret = gen_salt(48)
        redirect_uris = request.form.get('redirect_uris').split()

        client_id, client_secret, redirect_uris
        document = {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": redirect_uris,
        }
        client.db.clients.insert_one(document)
        return jsonify(client_id=client_id, client_secret=client_secret)
    return '''
        <form method="post">
            Redirect URIs: <input type="text" name="redirect_uris">
            <input type="submit">
        </form>
    '''
