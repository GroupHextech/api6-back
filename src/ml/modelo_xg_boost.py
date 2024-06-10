import re
import os
import string
import unicodedata
import pandas as pd
import numpy as np
import nltk
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from joblib import dump
import xgboost as xgb

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Define o diretório do script como diretório de trabalho atual
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Carrega o conjunto de dados
dataset = pd.read_csv("train.csv")
# Remove linhas com valores em branco
dataset = dataset.dropna(subset=['review_text', 'overall_rating'])
# Cria uma nova coluna para classificar entre comentários positivos(2), negativos(0) ou neutros(1) com base na nota:
dataset['feeling'] = np.where(dataset['overall_rating'] < 3, 0, np.where(dataset['overall_rating'] == 3, 1, 2))

# Criação da instância do lematizador e das stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('portuguese'))

# Lista para armazenar os textos pré-processados
preprocessed_texts = []

# Itera sobre cada texto no dataset para pré-processamento
for text in dataset['review_text']:
    # Verifica se o texto é uma string
    if isinstance(text, str):
        # Converte para minúsculas
        text = text.lower()
        # Remove acentos
        text = ''.join(char for char in unicodedata.normalize('NFKD', text) if unicodedata.category(char) != 'Mn')
        # Remove números usando expressão regular
        text = re.sub(r'\d+', '', text)
        # Remove caracteres especiais (incluindo emojis)
        text = re.sub(r'[^\w\s]', '', text)
        # Remove pontuação
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Remove espaços extras
        text = re.sub(r'\s+', ' ', text).strip()
        # Tokenização
        tokens = word_tokenize(text)
        # Lematização e remoção de stopwords
        tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word.lower() not in stop_words]
        # Junta os tokens em texto novamente
        preprocessed_text = ' '.join(tokens)
        # Adiciona o texto pré-processado à lista
        preprocessed_texts.append(preprocessed_text)
    else:
        preprocessed_texts.append("")

# Substitui os textos originais pelos textos já preparados para análise
dataset['review_text'] = preprocessed_texts

# Separa os dados em features (X) e target (Y)
X = dataset['review_text'].values
Y = dataset['feeling'].values

# Cria um objeto CountVectorizer com N-grams, considerando unigramas, bigramas e trigramas
ngram_vectorizer = CountVectorizer(ngram_range=(1, 3))

# Transforma os textos em vetores numéricos, representando a frequência de ocorrência de cada palavra e combinação de palavras
X_ngrams = ngram_vectorizer.fit_transform(X)

# Cria uma instância do modelo XGBoost
xgboost = xgb.XGBClassifier()

# Calcula os pesos de amostra com base nas classes
class_weights = np.zeros(len(Y))
class_counts = np.bincount(Y)
for i in range(len(class_counts)):
    class_weights[Y == i] = len(Y) / class_counts[i]

# Treina o modelo XGBoost com pesos de amostra
xgboost.fit(X_ngrams, Y, sample_weight=class_weights)

# Salva o modelo e o vetorizador em um único arquivo chamado 'modelo_xg_boost.joblib'
dump((xgboost, ngram_vectorizer), 'modelo_xg_boost.joblib')