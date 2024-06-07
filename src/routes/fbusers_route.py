from flask import Blueprint, jsonify, request
from ..database import firebase
from ..database import mongodb
from werkzeug.exceptions import BadRequest
import json
from datetime import datetime


# Crie um blueprint para a rota de blacklist
blueprint_fbusers = Blueprint("fbusers", __name__, url_prefix="/users")



@blueprint_fbusers.route('/backup', methods=['GET'])
def users_backup():
    try:
        users = firebase.get_all_users()
        deserialized_json = json.loads(users)

        now = datetime.now()

        # Criando o documento com os campos desejados
        document = {
            "day": now.day,
            "month": now.month,
            "year": now.year,
            "hour": now.hour,
            "minute": now.minute,
            "second": now.second,
            "data": [deserialized_json]
        }

        mongodb.client.db.users.insert_one(document)

        return jsonify(deserialized_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@blueprint_fbusers.route('/delete', methods=['GET'])
def users_delete():
    try:
        result = firebase.delete_all_users()
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint_fbusers.route('/restore')
def get_users():
    try:
        # Obtendo os parâmetros da query string
        year_param = request.args.get('year')
        month_param = request.args.get('month')
        day_param = request.args.get('day')

        # Convertendo os parâmetros para inteiros
        if year_param is not None:
            year_param = int(year_param)
        if month_param is not None:
            month_param = int(month_param)
        if day_param is not None:
            day_param = int(day_param)

        # Construindo o filtro
        filter_query = {}
        if year_param is not None:
            filter_query['year'] = year_param
        if month_param is not None:
            filter_query['month'] = month_param
        if day_param is not None:
            filter_query['day'] = day_param

        # Executando a consulta
        document = mongodb.client.db.users.find_one(filter_query)


        # Convertendo o documento para JSON e retornando
        if document:
            document['_id'] = str(document['_id'])  # Convertendo ObjectId para string
        
 
        result  = firebase.insert_users_from_json(document)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
