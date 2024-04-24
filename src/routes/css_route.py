from flask import Blueprint, jsonify, request, make_response
import requests
import time
import os
import mimetypes
import json
from io import BytesIO
from bson import json_util, ObjectId
from src.repositories.css_repository import *
from ..database import mongodb


blueprint_css = Blueprint("css", __name__, url_prefix="/css")

@blueprint_css.route('/test')
def test_route():
    # Carregar o modelo de análise de sentimentos
    sentiment_model = load_sentiment_model(model_path)

    # Verificar se o modelo foi carregado corretamente
    if sentiment_model is not None:
        # Fazer uma previsão de exemplo
        exemplo_texto = "Este é um ótimo dia!"
        resultado = sentiment_model.predict([exemplo_texto])
        return jsonify({"resultado": resultado.tolist()})  # Converter para lista para serialização JSON
    else:
        return jsonify({"erro": "O modelo não foi carregado corretamente."})

@blueprint_css.route('/categories')
def get_categories():
    try:
        pipeline = [{
            "$group": {
            "_id": "$site_category_lv1",
                "count": {"$sum": 1}  # Calculate total reviews per level 1 category
            }
        },
        {
            "$sort": {"count": -1}  # Sort by count descending (most to least reviews)
        },
        {
            "$limit": 10  # Limit to top 10 categories
        }]

        documents = client.db.css.aggregate(pipeline)
        result = {"list": list(documents)}

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@blueprint_css.route('/gender')
def get_gender():
    try:
        pipeline = [{
            "$group": {
                "_id": "$reviewer_gender",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        }]
        documents = client.db.css.aggregate(pipeline)
        result = {"list": list(documents)}

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint_css.route('/date')
def get_date():
    try:
        pipeline = [{
            "$group": {
            "_id": "$submission_date",
            "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        }]
        documents = client.db.css.aggregate(pipeline)
        result = {"list": list(documents)}

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint_css.route('/state')
def get_state():
    try:
        pipeline = [{
            "$group": {
            "_id": "$reviewer_state",
            "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        }]
        documents = client.db.css.aggregate(pipeline)
        result = {"list": list(documents)}

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint_css.route('/birth_year')
def get_birth_year():
    try:
        pipeline = [{
            "$group": {
            "_id": "$reviewer_birth_year",
            "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        }]
        documents = client.db.css.aggregate(pipeline)
        result = {"list": list(documents)}

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
