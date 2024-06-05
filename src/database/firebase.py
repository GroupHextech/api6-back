import os
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Carrega as credenciais do Firebase a partir das variáveis de ambiente
firebase_credentials = os.getenv('FIREBASE_CREDENTIALS')

if not firebase_credentials:
    raise ValueError("Credenciais do Firebase não encontradas. Por favor, defina a variável de ambiente 'FIREBASE_CREDENTIALS'.")

# Converte a string JSON para um dicionário Python
cred_dict = json.loads(firebase_credentials)

# Inicializa as credenciais do Firebase a partir do dicionário
cred = credentials.Certificate(cred_dict)

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
