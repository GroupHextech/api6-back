# models.py
from flask_pymongo import PyMongo
from ..database.mongodb import *

def save(token):
    client.db.tokens.insert_one(token)

def get(access_token):
    return client.db.tokens.find_one({'access_token': access_token})

def delete(access_token):
    client.db.tokens.delete_one({'access_token': access_token})
