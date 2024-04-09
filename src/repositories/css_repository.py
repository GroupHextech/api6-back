from ..database.mongodb import mongo


def get_all_documents():
    collection = mongo.db.css
    documents = collection.find({})
    return documents
