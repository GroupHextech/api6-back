from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app):
    return mongo.init_app(app)


#from pymongo import MongoClient

#def get_mongo_client(uri):
  #  return MongoClient(uri)

#def get_collection(client, db_name, collection_name):
   # db = client[db_name]
   # return db[collection_name]