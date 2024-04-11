from ..database.collections import *


def get_all_documents():
    documents = collection_css.find({})
    return documents
