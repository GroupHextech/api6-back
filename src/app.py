from flask import Flask, jsonify
from flask_cors import CORS
import warnings
import os
from .routes import blueprint_review
from .database import mongodb, firebase
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb+srv://admin:1234@api6.u8duoyj.mongodb.net/develop?ssl=true&retryWrites=true&w=majority&appName=Api6"
CORS(app)

# Register blueprint
app.register_blueprint(blueprint_review)

# Inicia o Mongo
mongodb.init_db(app)

# Inicia o Firebase
firebase_admin.initialize_app(firebase.cred)

if __name__ == "__main__":
    app.run()
