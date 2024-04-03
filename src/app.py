from flask import Flask
from flask_cors import CORS
import warnings
import os
from .utils import *
from .controller import *
 
app = Flask(__name__)

CORS(app)

app.register_blueprint(blueprint1)
 

 