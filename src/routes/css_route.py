from flask import Blueprint, jsonify, request, make_response
import requests
import time
import os
import mimetypes
import json
from io import BytesIO
from bson import json_util, ObjectId
from ..repositories.css_repository import *


blueprint_css = Blueprint("css", __name__, url_prefix="/css")

@blueprint_css.route('/all')
def get_all():
    try:
        documents = get_all_documents()
        cont = 0
        result = {"list": []}

        for doc in documents:
            data = {
                'submission_date': doc.get('submission_date'),
                'reviewer_id': doc.get('reviewer_id'),
                'product_id': doc.get('product_id'),
                'product_name': doc.get('product_name'),
                'product_brand': doc.get('product_brand'),
                'site_category_lv1': doc.get('site_category_lv1'),
                'site_category_lv2': doc.get('site_category_lv2'),
                'review_title': doc.get('review_title'),
                'overall_rating': doc.get('overall_rating'),
                'recommend_to_a_friend': doc.get('recommend_to_a_friend'),
                'review_text': doc.get('review_text'),
                'reviewer_birth_year': doc.get('reviewer_birth_year'),
                'reviewer_gender': doc.get('reviewer_gender'),
                'reviewer_state': doc.get('reviewer_state')
            }
            if cont < 34581:
                result["list"].append(data)
                cont += 1

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

"""
@blueprint_css.route('/date')
def get_date():
    documents = get_all()
    list = []
    for doc in documents:
        if 'submission_date' in doc:
            list.append(doc['submission_date'])
            
    result = {"list": list}
    return jsonify(result)

@blueprint_css.route('/reviewer_id')
def get_reviewer_id():
    documents = get_all()
    list = []
    for doc in documents:
        if 'reviewer_id' in doc:
            list.append(doc['reviewer_id'])
            
    result = {"list": list}
    return jsonify(result)

@blueprint_css.route('/product_id')
def get_product_id():
    documents = get_all()
    list = []
    for doc in documents:
        if 'product_id' in doc:
            list.append(doc['product_id'])
            
    result = {"list": list}
    return jsonify(result)

@blueprint_css.route('/product_name')
def get_product_name():
    documents = get_all()
    list = []
    for doc in documents:
        if 'product_name' in doc:
            list.append(doc['product_name'])
            
    result = {"list": list}
    return jsonify(result)

@blueprint_css.route('/brand')
def get_brand():
    documents = get_all()
    list = []
    for doc in documents:
        if 'product_brand' in doc:
            list.append(doc['product_brand'])
            
    result = {"list": list}
    return jsonify(result)

@blueprint_css.route('/category1')
def get_category1():
    documents = get_all()
    list = []
    for doc in documents:
        if 'site_category_lv1' in doc:
            list.append(doc['site_category_lv1'])
            
    result = {"list": list}
    return jsonify(result)

@blueprint_css.route('/category2')
def get_category2():
    documents = get_all()
    list = []
    for doc in documents:
        if 'site_category_lv2' in doc:
            list.append(doc['site_category_lv2'])
            
    result = {"list": list}
    return jsonify(result)

@blueprint_css.route('/title')
def get_title():
    documents = get_all()
    list = []
    for doc in documents:
        if 'review_title' in doc:
            list.append(doc['review_title'])
            
    result = {"list": list}
    return jsonify(result)

@blueprint_css.route('/rating')
def get_rating():
    documents = get_all()
    list = []
    for doc in documents:
        if 'overall_rating' in doc:
            list.append(doc['overall_rating'])
            
    result = {"list": list}
    return jsonify(result)

@blueprint_css.route('/recommend')
def get_recommend():
    documents = get_all()
    list = []
    for doc in documents:
        if 'recommend_to_a_friend' in doc:
            list.append(doc['recommend_to_a_friend'])
            
    result = {"list": list}
    return jsonify(result)

@blueprint_css.route('/text')
def get_text():
    documents = get_all()
    list = []
    for doc in documents:
        if 'review_text' in doc:
            list.append(doc['review_text'])
            
    result = {"list": list}
    return jsonify(result)

@blueprint_css.route('/birth')
def get_birth():
    documents = get_all()
    list = []
    for doc in documents:
        if 'reviewer_birth_year' in doc:
            list.append(doc['reviewer_birth_year'])
            
    result = {"list": list}
    return jsonify(result)

@blueprint_css.route('/gender')
def get_gender():
    documents = get_all()
    list = []
    for doc in documents:
        if 'reviewer_gender' in doc:
            list.append(doc['reviewer_gender'])
            
    result = {"list": list}
    return jsonify(result)

@blueprint_css.route('/state')
def get_state():
    documents = get_all()
    list = []
    for doc in documents:
        if 'reviewer_state' in doc:
            list.append(doc['reviewer_state'])
            
    result = {"list": list}
    return jsonify(result)
"""