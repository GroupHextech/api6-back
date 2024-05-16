from ..database.mongodb import *
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string


def get_all_documents():
    collection_review = client.db.review
    documents = collection_review.find({})
    return documents

def calculate_word_frequency(feeling=None, state=None):
    # Conexão com o banco de dados MongoDB
    collection_review = client.db.review
    # Inicializa uma lista para armazenar os textos dos reviews
    reviews = []
    # Define um filtro inicial
    filter_query = {}
    # Adiciona filtros com base nos parâmetros de consulta
    if feeling:
        filter_query['Feeling_Predicted'] = feeling
    if state:
        filter_query['reviewer_state'] = state
    # Itera sobre os documentos na coleção com base no filtro
    for doc in collection_review.find(filter_query):
        # Verifica se o campo 'review_text' está presente no documento
        if 'review_text' in doc:
            # Se o campo 'review_text' estiver presente, adiciona o texto à lista de reviews
            reviews.append(doc['review_text'])
    # Concatena todos os textos em uma única string
    text = ' '.join(reviews)
    # Tokeniza o texto em palavras
    words = word_tokenize(text)
    # Remove pontuação
    words = [word for word in words if word not in string.punctuation]
    # Carrega as stopwords da língua portuguesa
    stopwords_list = set(stopwords.words('portuguese'))
    # Adiciona palavras adicionais a serem removidas
    additional_stopwords = ["Produto", "produto", "...", "pra"]  # Adicione outras palavras conforme necessário
    # Remove stopwords padrão e palavras adicionais
    words = [word for word in words if word.lower() not in stopwords_list and word.lower() not in additional_stopwords]
    # Calcula a frequência das palavras
    word_freq = Counter(words)
    # Retorna as 25 palavras mais comuns
    return word_freq.most_common(25)