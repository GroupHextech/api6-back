from flask import Blueprint, jsonify, request, make_response
from ..database import firebase
from werkzeug.exceptions import BadRequest

# Crie um blueprint para a rota de blacklist
blueprint_blacklist = Blueprint("blacklist", __name__, url_prefix="/blacklist")

@blueprint_blacklist.route('/all', methods=['GET'])
def get_all():
    # Referência para a coleção 'blacklist'
    blacklist_ref = firebase.fbd.collection('blacklist')

    try:
        # Obter todos os documentos da coleção
        docs = blacklist_ref.stream()

        # Extrair os dados dos documentos obtidos
        blacklist_items = [doc.to_dict() for doc in docs]

        # Retornar os dados em formato JSON
        return jsonify(blacklist_items), 200
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
