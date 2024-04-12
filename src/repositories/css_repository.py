from ..database.mongodb import *


def get_all_documents():
    collection_css = client.db.css
    documents = collection_css.find({})
    return documents

def get_categories_documents():
    collection_css = client.db.css
    documents = collection_css.find({'site_category_lv1': {'$exists': True}, 'site_category_lv2': {'$exists': True}})
    return documents

def get_gender_documents():
    collection_css = client.db.css
    documents = collection_css.find({'reviewer_gender': {'$exists': True}})
    return documents

def get_date_documents():
    collection_css = client.db.css
    documents = collection_css.find({'submission_date': {'$exists': True}})
    return documents

def get_state_documents():
    collection_css = client.db.css
    documents = collection_css.find({'reviewer_state': {'$exists': True}})
    return documents

def get_birth_year_documents():
    collection_css = client.db.css
    documents = collection_css.find({'reviewer_birth_year': {'$exists': True}})
    return documents
