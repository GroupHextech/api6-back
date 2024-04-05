from flask import Flask
from flask_cors import CORS
import warnings
import os
from .routes import *
from .database import mongodb
from dotenv import load_dotenv


def create_app(config_object="src.settings"):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config_object)    
    CORS(app)
    mongodb.init_db(app)
    app.register_blueprint(blueprint1)
    return app
