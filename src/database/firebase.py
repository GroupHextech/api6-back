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

def delete_all_users():
    fclient = init_firestore()
    if fclient:
        try:
            users_ref = fclient.collection('users')
            docs = users_ref.stream()
            for doc in docs:
                print(f"Deletando usuário com ID: {doc.id}")
                doc.reference.delete()
            print("Todos os usuários foram deletados com sucesso.")
            return "Todos os usuários foram deletados com sucesso."
        except Exception as e:
            print(f"Erro ao deletar usuários: {e}")

def delete_one_user(userid):
    fclient = init_firestore()
    if fclient:
        try:
            users_ref = fclient.collection('users')
            docs = users_ref.stream()
            for doc in docs:
                if doc.id == userid:
                    doc.reference.delete()           
            return "Usuário removido com sucesso."
        except Exception as e:
            print(f"Erro ao deletar usuários: {e}")

def insert_users_from_json(json_data, blacklist):     
    fclient = init_firestore()
    if fclient:
        inserted_ids = []
        try:
            result_delete = delete_all_users()
            print(blacklist)
            print(blacklist)
            #data = json.loads(json_data)
            users_data = json_data.get('data', [])
            if users_data:
                for user_batch in users_data:
                    for user_id, user_info in user_batch.items():
                        if user_id in blacklist:
                            print(f"O user_id {user_id} está na lista.")
                        else:
                            user_info['createdAt'] = firestore.SERVER_TIMESTAMP if user_info.get('createdAt') is None else user_info['createdAt']
                            fclient.collection('users').document(user_id).set(user_info)
                            inserted_ids.append(user_id)
                            #print(f"Usuário {user_id} adicionado com sucesso.")
                        
            return json.dumps(inserted_ids)
        except Exception as e:
            print(f"Erro ao inserir usuários: {e}")



# Listando todas as coleções
#list_collections()
#get_all_users()
