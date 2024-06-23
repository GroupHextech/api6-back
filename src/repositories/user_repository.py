from flask_pymongo import PyMongo
from ..database.mongodb import *
import bcrypt

def get(user_id):
    return client.db.users.find_one({'_id': user_id})

def validate(username, password):
    return client.db.users.find_one({'username': username, 'password': password})

# Função para criar um novo usuário no MongoDB
def create_user(username, password, scopes):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_data = {
        'username': username,
        'password': hashed_password,
        'scopes': scopes
    }
    client.db.users_oauth.insert_one(user_data)

# Função para autenticar um usuário
def authenticate_user(username, password):
    user_data = client.db.users_oauth.find_one({'username': username})
    # return user_data
    if user_data and bcrypt.checkpw(password.encode('utf-8'), bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())):
        return user_data
    