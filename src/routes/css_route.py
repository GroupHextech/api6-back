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
