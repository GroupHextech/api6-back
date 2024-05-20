from ..database.mongodb import *
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from functools import lru_cache


def get_all_documents():
    collection_review = client.db.review
    documents = collection_review.find({})
    return documents

def calculate_word_frequency(feeling=None, state=None):

    # Conexão com o banco de dados MongoDB
    collection_review = client.db.review

    # Define um filtro inicial
    filter_query = {}

    # Adiciona filtros com base nos parâmetros de consulta
    if feeling:
        filter_query['Feeling_Predicted'] = feeling
    if state:
        filter_query['reviewer_state'] = state

    cursor = collection_review.find(filter_query, {'review_text': 1})

    # Carrega as stopwords da língua portuguesa
    stopwords_list = set(stopwords.words('portuguese'))

    # Adiciona palavras adicionais a serem removidas
    additional_stopwords = ["Produto", "produto", "...", "pra"]
    stopwords_list.update(additional_stopwords)

    word_freq = Counter()

    for doc in cursor:
        if 'review_text' in doc:
            words = word_tokenize(doc['review_text'])
            words = [word.lower() for word in words if word.isalnum() and word.lower() not in stopwords_list]
            word_freq.update(words)

    return word_freq.most_common(25)

@lru_cache(maxsize=128)
def cached_calculate_word_frequency(feeling=None, state=None):
    return calculate_word_frequency(feeling, state)