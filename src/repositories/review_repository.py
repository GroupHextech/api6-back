from ..database.mongodb import *


def get_all_documents():
    collection_review = client.db.review
    documents = collection_review.find({})
    return documents
