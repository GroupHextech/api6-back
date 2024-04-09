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


 
@blueprint1.route('/all')
def get_data():
    try:
        collection = mongo.db.css
        ocuments = collection.find({})
        documents = get_all_documents()
        contador = 0
        list = []
        for doc in documents:
            doc['_id'] = str(doc['_id'])
            if contador < 500:
                list.append(doc)
            contador = contador +1
            #if 'reviewer_state' in doc:
                #list.append(doc['reviewer_state'])
            
        result = {"list": list}
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


  
