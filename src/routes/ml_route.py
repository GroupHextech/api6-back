from flask import Blueprint, jsonify, request, make_response
import requests
import time
import os
import mimetypes
import json
from flask import Blueprint, jsonify
from joblib import load
import pandas as pd
from io import BytesIO
from bson import json_util, ObjectId
from src.repositories.ml_repository import *


blueprint_ml = Blueprint("ml", __name__, url_prefix="/ml")

@blueprint_ml.route('/feeling')
def get_feeling():
    try:
        state_params = request.args.getlist('state')
        region_param = request.args.get('region')
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

        model_ngrams, ngram_vectorizer, df_combined = load_sentiment_model()

        # Converter df_results_true_count para um dicionário
        df_combined = df_combined.to_dict()

        # Retornar o dicionário como JSON
        return jsonify(df_combined)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint_ml.route('/feeling_count')
def get_feeling_count():
    try:
        state_params = request.args.getlist('state')
        region_param = request.args.get('region')
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

        model_ngrams, ngram_vectorizer, df_combined = load_sentiment_model()

        # Contagem de valores para 'Feeling_Predicted'
        feeling_predicted_counts = df_combined['Feeling_Predicted'].value_counts()

        # Converter df_results_true_count para um dicionário
        df_combined = feeling_predicted_counts .to_dict()

        # Retornar o dicionário como JSON
        return jsonify(feeling_predicted_counts)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
