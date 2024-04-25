from ..database.mongodb import *


def get_all_documents():
    collection_css = client.db.css
    documents = collection_css.find({})
    return documents
