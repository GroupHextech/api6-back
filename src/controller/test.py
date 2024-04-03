from flask import Blueprint, jsonify, request, make_response
import requests
import time
import os
import mimetypes
import json
from io import BytesIO

from src.utils.mongodb import get_mongo_client, get_collection

#Importamos json_util do pacote bson (que é parte do pymongo) para ajudar na serialização dos objetos 
#do MongoDB para JSON.
from bson import json_util, ObjectId



blueprint1 = Blueprint("test1", __name__, url_prefix="/api")

MONGO_URI = "mongodb+srv://admin:1234@api6.u8duoyj.mongodb.net/?retryWrites=true&w=majority&appName=Api6"
DB_NAME = "sample_mflix"
COLLECTION_NAME = "comments"

@blueprint1.route('/test')
def hello_world():
    return 'Hello, World!'

@blueprint1.route('/data')
def get_data():
    mongo_client = get_mongo_client(MONGO_URI)
    collection = get_collection(mongo_client, DB_NAME, COLLECTION_NAME)
    data = list(collection.find({}))  # Obtém todos os documentos (exemplo)
    #return jsonify(data)  # Converte os dados para JSON e retorna
    # Primeiro, usamos json_util.dumps para converter a lista de documentos (incluindo ObjectIds e outros tipos) 
    #em uma string JSON. Depois, usamos json.loads para converter essa string JSON de volta para um formato 
    #que o jsonify do Flask pode manipular e enviar como uma resposta HTTP.
    return jsonify(json.loads(json_util.dumps(data)))