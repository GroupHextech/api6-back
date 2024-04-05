from flask import Blueprint, jsonify, request, make_response
import requests
import time
import os
import mimetypes
import json
from io import BytesIO
from bson import json_util, ObjectId
from ..repositories.css_repository import *


blueprint1 = Blueprint("test1", __name__, url_prefix="/api")

@blueprint1.route('/test')
def hello_world():
    return 'Hello, World!'

@blueprint1.route('/data')
def get_data():
    #collection = mongo.db.css
    #ocuments = collection.find({})
    documents = get_all_documents()
    list = []
    for doc in documents:
        if 'reviewer_state' in doc:
            list.append(doc['reviewer_state'])
            
    result = {"list": list}
    return jsonify(result)
