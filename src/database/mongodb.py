from flask_pymongo import PyMongo

client = PyMongo()

def init_db(app):
    return client.init_app(app)