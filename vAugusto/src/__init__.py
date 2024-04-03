from flask import Flask
from pymongo import MongoClient
from .config import MONGO_URI

app = Flask(__name__)

client = MongoClient(MONGO_URI)
db = client.get_default_database()
