import os
from firebase_admin import credentials

# caminho cahve firebase
cred = credentials.Certificate(
    os.path.join(
        os.path.dirname(__file__),
        "D:\\Codigos\\Fatec\\api6\\firebase\\hex-imagem-firebase-adminsdk-us6mv-b020efced9.json"
    )
)
