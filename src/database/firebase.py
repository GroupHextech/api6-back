import os
import firebase_admin
from firebase_admin import credentials, firestore
import json


# caminho cahve firebase
cred = credentials.Certificate(
    os.path.join(
        os.path.dirname(__file__),
        #r"C:\\temporario\\api6_fatec\\api-sprint3\\api6-back\\src\\firebase.json"
    )
)

firebase_app = firebase_admin.initialize_app(cred)

def init_firestore():
    fclient = firestore.client(app=firebase_app)
    return fclient

def list_collections():
    fclient = init_firestore()
    collections = fclient.collections()
    for collection in collections:
        print(f'Collection ID: {collection.id}')


def get_all_users():
    fclient = init_firestore()
    users_ref = fclient.collection('users')
    docs = users_ref.stream()
    all_users = {}
    for doc in docs:
        all_users[doc.id] = doc.to_dict()
    # Convertendo o dicionário para JSON
    all_users_json = json.dumps(all_users, default=str)
    return all_users_json

# Listando todas as coleções
#list_collections()
#get_all_users()
