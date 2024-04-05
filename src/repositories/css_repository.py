from ..database.mongodb import mongo


def get_all():
    collection = mongo.db.css
    documents = collection.find({})
    return documents
