import os
import firebase_admin
from firebase_admin import credentials, firestore

# caminho cahve firebase
cred = credentials.Certificate(
    os.path.join(
        os.path.dirname(__file__),
        r"D:\\Codigos\\Fatec\\api6\\firebase\\hex-imagem-firebase-adminsdk-us6mv-b020efced9.json"
    )
)

firebase_app = firebase_admin.initialize_app(cred)

def init_firestore():
    fclient = firestore.client(app=firebase_app)
    return fclient

fbd = firestore.client()
