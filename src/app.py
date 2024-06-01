from flask import Flask, jsonify
from flask_cors import CORS
import warnings
import os
from .routes import blueprint_review, blueprint_blacklist, blueprint_fbusers, bp_generate, bp_verify
from .database import mongodb, firebase
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb+srv://admin:1234@api6.u8duoyj.mongodb.net/develop?ssl=true&retryWrites=true&w=majority&appName=Api6"
CORS(app)

# Inicia o Mongo
mongodb.init_db(app)

# Register blueprint
app.register_blueprint(blueprint_review)
app.register_blueprint(blueprint_blacklist)
app.register_blueprint(blueprint_fbusers)
app.register_blueprint(bp_generate)
app.register_blueprint(bp_verify)

# Inicia o Firebase
firebase.init_firestore()

if __name__ == "__main__":
    app.run()
