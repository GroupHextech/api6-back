from flask_pymongo import PyMongo

client = PyMongo()

def init_db(app):
    return client.init_app(app)

def get_user_secrets_collection():
    return client.db.user_secrets