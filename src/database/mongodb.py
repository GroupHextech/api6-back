from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app):
    return mongo.init_app(app)
