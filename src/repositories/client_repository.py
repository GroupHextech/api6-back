from ..database.mongodb import *

def get(client_id):
    return client.db.clients.find_one({'client_id': client_id})

def save(client_id, client_secret, redirect_uris):
    client.db.clients.insert_one({
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uris': redirect_uris
    })
