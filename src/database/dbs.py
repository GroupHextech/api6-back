from flask_pymongo import PyMongo


develop = PyMongo()

def init_db(app):
    return develop.init_app(app)
