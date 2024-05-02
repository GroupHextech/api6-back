from flask import Flask
from flask_cors import CORS
import warnings
import os
from .routes import *
from .database import mongodb
from dotenv import load_dotenv


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://admin:1234@api6.u8duoyj.mongodb.net/develop?ssl=true&retryWrites=true&w=majority&appName=Api6"
CORS(app)
app.register_blueprint(blueprint_review)
mongodb.init_db(app)


if __name__ == "__main__":
    app.run()
