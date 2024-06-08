from flask import Blueprint, jsonify, redirect, request, make_response
import requests
import time
import os
import mimetypes
import json
from io import BytesIO
from bson import json_util, ObjectId
from src.repositories.review_repository import *
from src.repositories.ml_repository import *
from ..database import mongodb
from werkzeug.exceptions import BadRequest


blueprint_review = Blueprint("review", __name__, url_prefix="/api")

@blueprint_review.route('/categories')
def get_categories():
    try:
        state_params = request.args.getlist('state')
        region_param = request.args.get('region')
        feeling_param = request.args.get('feeling')
        #print (state_params)
        filter_query = {}

        if region_param:
            state_params = []
            if region_param == 'sudeste':
                state_params = ['SP', 'MG', 'RJ', 'ES']
            elif region_param == 'sul':
                state_params = ['PR', 'RS', 'SC']
            elif region_param == 'centro-oeste':
                state_params = ['DF', 'GO', 'MT', 'MS']
            elif region_param == 'norte':
                state_params = ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO']
            elif region_param == 'nordeste':
                state_params = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'RN', 'SE']
            else:
                state_params = []

        if state_params:
            filter_query['reviewer_state']={"$in": state_params}
        
        if feeling_param:   
            filter_query['Feeling_Predicted'] = feeling_param

        pipeline = [
        {
            "$match": filter_query 
        },
        {
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

        documents = client.db.review.aggregate(pipeline)
        result = {"list": list(documents)}

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint_review.route('/gender')
def get_gender():
    try:
        state_params = request.args.getlist('state')
        region_param = request.args.get('region')
        feeling_param = request.args.get('feeling')
        #print (state_params)
        filter_query = {}

        if region_param:
            state_params = []
            if region_param == 'sudeste':
                state_params = ['SP', 'MG', 'RJ', 'ES']
            elif region_param == 'sul':
                state_params = ['PR', 'RS', 'SC']
            elif region_param == 'centro-oeste':
                state_params = ['DF', 'GO', 'MT', 'MS']
            elif region_param == 'norte':
                state_params = ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO']
            elif region_param == 'nordeste':
                state_params = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'RN', 'SE']
            else:
                state_params = []

        if state_params:
            filter_query['reviewer_state']={"$in": state_params}
        
        if feeling_param:  # Novo filtro baseado no parâmetro "feeling"
            filter_query['Feeling_Predicted'] = feeling_param

        pipeline = [
        {
            "$match": filter_query 
        },
        {
            "$group": {
                "_id": "$reviewer_gender",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        }]
        documents = client.db.review.aggregate(pipeline)
        result = {"list": list(documents)}

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint_review.route('/date')
def get_date():
    try:
        state_params = request.args.getlist('state')
        region_param = request.args.get('region')
        feeling_param = request.args.get('feeling')
        #print (state_params)
        filter_query = {}

        if region_param:
            state_params = []
            if region_param == 'sudeste':
                state_params = ['SP', 'MG', 'RJ', 'ES']
            elif region_param == 'sul':
                state_params = ['PR', 'RS', 'SC']
            elif region_param == 'centro-oeste':
                state_params = ['DF', 'GO', 'MT', 'MS']
            elif region_param == 'norte':
                state_params = ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO']
            elif region_param == 'nordeste':
                state_params = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'RN', 'SE']
            else:
                state_params = []

        if state_params:
            filter_query['reviewer_state']={"$in": state_params}
        
        if feeling_param:   
            filter_query['Feeling_Predicted'] = feeling_param
            
        pipeline = [
        {
            "$match": filter_query 
        },
        {
            "$group": {
            "_id": "$submission_date",
            "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        }]
        documents = client.db.review.aggregate(pipeline)
        result = {"list": list(documents)}

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint_review.route('/state')
def get_state():
    try:
        state_params = request.args.getlist('state')
        region_param = request.args.get('region')
        feeling_param = request.args.get('feeling')
        #print (state_params)
        filter_query = {}

        if region_param:
            state_params = []
            if region_param == 'sudeste':
                state_params = ['SP', 'MG', 'RJ', 'ES']
            elif region_param == 'sul':
                state_params = ['PR', 'RS', 'SC']
            elif region_param == 'centro-oeste':
                state_params = ['DF', 'GO', 'MT', 'MS']
            elif region_param == 'norte':
                state_params = ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO']
            elif region_param == 'nordeste':
                state_params = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'RN', 'SE']
            else:
                state_params = []

        if state_params:
            filter_query['reviewer_state']={"$in": state_params}
        
        if feeling_param:   
            filter_query['Feeling_Predicted'] = feeling_param

        pipeline = [
        {
            "$match": filter_query 
        },
        {
            "$group": {
            "_id": "$reviewer_state",
            "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        }]
        documents = client.db.review.aggregate(pipeline)
        result = {"list": list(documents)}

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint_review.route('/birth_year')
def get_birth_year():
    try:
        state_params = request.args.getlist('state')
        region_param = request.args.get('region')
        feeling_param = request.args.get('feeling')
        #print (state_params)
        filter_query = {}

        if region_param:
            state_params = []
            if region_param == 'sudeste':
                state_params = ['SP', 'MG', 'RJ', 'ES']
            elif region_param == 'sul':
                state_params = ['PR', 'RS', 'SC']
            elif region_param == 'centro-oeste':
                state_params = ['DF', 'GO', 'MT', 'MS']
            elif region_param == 'norte':
                state_params = ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO']
            elif region_param == 'nordeste':
                state_params = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'RN', 'SE']
            else:
                state_params = []
        
        if state_params:
            filter_query['reviewer_state']={"$in": state_params}
        
        if feeling_param:   
            filter_query['Feeling_Predicted'] = feeling_param

        pipeline = [
        {
            "$match": filter_query 
        },
        {
            "$group": {
            "_id": "$reviewer_birth_year",
            "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        }]
        documents = client.db.review.aggregate(pipeline)
        result = {"list": list(documents)}

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint_review.route('/feeling_ml')
def get_feeling_ml():
    try:
        state_params = request.args.getlist('state')
        region_param = request.args.get('region')
        feeling_param = request.args.get('feeling')
        #print (state_params)
        filter_query = {}

        if region_param:
            state_params = []
            if region_param == 'sudeste':
                state_params = ['SP', 'MG', 'RJ', 'ES']
            elif region_param == 'sul':
                state_params = ['PR', 'RS', 'SC']
            elif region_param == 'centro-oeste':
                state_params = ['DF', 'GO', 'MT', 'MS']
            elif region_param == 'norte':
                state_params = ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO']
            elif region_param == 'nordeste':
                state_params = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'RN', 'SE']
            else:
                state_params = []
        
        if state_params:
            filter_query['reviewer_state']={"$in": state_params}
        
        if feeling_param:   
            filter_query['Feeling_Predicted'] = feeling_param

        pipeline = [
        {
            "$match": filter_query 
        },
        {
            "$group": {
            "_id": "$Feeling_Predicted",
            "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        }]
        documents = client.db.review.aggregate(pipeline)
        result = {"list": list(documents)}

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint_review.route('/feeling')
def get_feeling():
    try:
        state_params = request.args.getlist('state')
        region_param = request.args.get('region')
        feeling_param = request.args.get('feeling')
        #print (state_params)
        filter_query = {}

        if region_param:
            state_params = []
            if region_param == 'sudeste':
                state_params = ['SP', 'MG', 'RJ', 'ES']
            elif region_param == 'sul':
                state_params = ['PR', 'RS', 'SC']
            elif region_param == 'centro-oeste':
                state_params = ['DF', 'GO', 'MT', 'MS']
            elif region_param == 'norte':
                state_params = ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO']
            elif region_param == 'nordeste':
                state_params = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'RN', 'SE']
            else:
                state_params = []
        
        if state_params:
            filter_query['reviewer_state']={"$in": state_params}
        
        if feeling_param:   
            filter_query['Feeling_Predicted'] = feeling_param

        pipeline = [
        {
            "$match": filter_query 
        },
        {
            "$group": {
            "_id": "$Feeling_Predicted",
            "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        }]
        documents = client.db.review.aggregate(pipeline)
        result = {"list": list(documents)}

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@blueprint_review.route('/feeling_by_month')
def get_feeling_by_month():
    try:
        state_params = request.args.getlist('state')
        region_param = request.args.get('region')
        feeling_param = request.args.get('feeling')
        filter_query = {}

        if region_param:
            state_params = []
            if region_param == 'sudeste':
                state_params = ['SP', 'MG', 'RJ', 'ES']
            elif region_param == 'sul':
                state_params = ['PR', 'RS', 'SC']
            elif region_param == 'centro-oeste':
                state_params = ['DF', 'GO', 'MT', 'MS']
            elif region_param == 'norte':
                state_params = ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO']
            elif region_param == 'nordeste':
                state_params = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'RN', 'SE']
            else:
                state_params = []
        
        if state_params:
            filter_query['reviewer_state']={"$in": state_params}

        if feeling_param:   
            filter_query['Feeling_Predicted'] = feeling_param

        # Create a new pipeline for grouping by month
        pipeline = [
            {
                "$addFields": {
                    "submission_month": {
                        "$dateFromString": {
                            "dateString": "$submission_date",
                            "format": "%Y-%m-%d %H:%M:%S"
                        }
                    }
                }
            },
            {
                "$match": filter_query 
            },
            {
                "$group": {
                    "_id": {"$dateToString": {"format": "%b", "date": "$submission_month"}},
                    "Negative": {"$sum": {"$cond": [{"$eq": ["$Feeling_Predicted", "Negative"]}, 1, 0]}},
                    "Neutral": {"$sum": {"$cond": [{"$eq": ["$Feeling_Predicted", "Neutral"]}, 1, 0]}},
                    "Positive": {"$sum": {"$cond": [{"$eq": ["$Feeling_Predicted", "Positive"]}, 1, 0]}}
                }
            },
            {
                "$addFields": {
                    "month_order": {
                        "$switch": {
                            "branches": [
                                {"case": {"$eq": ["$_id", "Jan"]}, "then": 1},
                                {"case": {"$eq": ["$_id", "Feb"]}, "then": 2},
                                {"case": {"$eq": ["$_id", "Mar"]}, "then": 3},
                                {"case": {"$eq": ["$_id", "Apr"]}, "then": 4},
                                {"case": {"$eq": ["$_id", "May"]}, "then": 5}
                            ],
                            "default": 0
                        }
                    }
                }
            },
            {
                "$sort": {"month_order": 1}
            },
            {
                "$project": {"Negative": 1, "Neutral": 1, "Positive": 1}
            }
        ]

        documents = client.db.review.aggregate(pipeline)
        result = {"list": list(documents)}

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint_review.route('/word-frequency')
def word_frequency():
    try:
        # Obtém os parâmetros de consulta
        feeling_param = request.args.get('feeling')
        state_param = request.args.get('state')

        # Verificar se os resultados pré-computados estão disponíveis
        precomputed_result = client.db.precomputed_results.find_one({
            'type': 'word_frequency',
            'feeling': feeling_param,
            'state': state_param
        })

        if precomputed_result:
            # Se os resultados pré-computados estiverem disponíveis, retornar esses resultados
            word_frequency_result = precomputed_result['result']
            word_frequency_dict = dict(word_frequency_result)
            return jsonify(word_frequency_dict)
        else:
            # Se não houver resultados pré-computados, calcular os resultados e retorná-los
            word_frequency_result = cached_calculate_word_frequency(feeling=feeling_param, state=state_param)
            word_frequency_dict = dict(word_frequency_result)

            client.db.precomputed_results.insert_one({
                'type': 'word_frequency',
                'feeling': feeling_param,
                'state': state_param,
                'result': word_frequency_dict
            })
            
            return jsonify(word_frequency_dict)

    except BadRequest as e:
        return make_response(jsonify({'error': str(e)}), 400)

    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

# Rota para processar o upload do CSV no Blueprint
@blueprint_review.route('/csv', methods=['POST'])
def upload_csv():
    # Check if file is present in the request
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return "No selected file", 400

    if file:
        # Save the file to a temporary location
        file_path = "temp.csv"
        file.save(file_path)

        # Call add_feelings function with appropriate arguments
        add_feelings(
            r"C:\Users\augus\Documents\VsCode\fatec\api6\HEXTECH-API6sem\api6-back\src\ml\modelo_xg_boost.joblib",
            file_path
        )

        os.remove(file_path)

        return "File uploaded and processed successfully", 200

    return "Something went wrong", 500
