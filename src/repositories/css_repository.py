from src.database.collections import *


def find_all():
    collection_css.find({})
    return collection_css
