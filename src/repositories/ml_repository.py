import os
import re
import string
import unicodedata
import numpy as np
import pandas as pd
import csv
from joblib import load
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from src.database.mongodb import client

def load_sentiment_model(caminho_modelo):
    xgboost, ngram_vectorizer = load(caminho_modelo)
    return xgboost, ngram_vectorizer

def formatar_csv(caminho_csv):
    dataset = pd.read_csv(caminho_csv, encoding='utf-8', low_memory=False, dtype=str)

    # Preencher valores vazios em todas as colunas com strings vazias
    dataset = dataset.fillna('')

    # Converter coluna 'overall_rating' para float e tratar valores inválidos
    dataset['overall_rating'] = pd.to_numeric(dataset['overall_rating'], errors='coerce')
    dataset = dataset.dropna(subset=['overall_rating'])
    dataset['overall_rating'] = dataset['overall_rating'].astype(float)

    # Criar nova coluna 'feeling' com base na coluna 'overall_rating'
    dataset['feeling'] = np.where(
        dataset['overall_rating'] < 3, 0,
        np.where(dataset['overall_rating'] == 3, 1, 2)
    )

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('portuguese'))

    preprocessed_texts = []

    for text in dataset['review_text']:
        if isinstance(text, str):
            text = text.lower()
            text = ''.join(char for char in unicodedata.normalize('NFKD', text) if unicodedata.category(char) != 'Mn')
            text = re.sub(r'\d+', '', text)
            text = re.sub(r'[^\w\s]', '', text)
            text = text.translate(str.maketrans('', '', string.punctuation))
            text = re.sub(r'\s+', ' ', text).strip()
            tokens = word_tokenize(text)
            tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word.lower() not in stop_words]
            preprocessed_text = ' '.join(tokens)
            preprocessed_texts.append(preprocessed_text)
        else:
            preprocessed_texts.append("")

    dataset['review_text'] = preprocessed_texts
    dataset.to_csv("C:\\csv_formatado.csv", index=False, encoding='utf-8')

    return dataset

def processar_coluna(df, column_name):
    df[column_name] = df[column_name].astype(str)
    df[column_name] = df[column_name].fillna('')

def insert_csv_to_mongodb(filepath):
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            client.db.review.insert_one(row)

def add_feelings(caminho_modelo, caminho_csv):
    xgboost, ngram_vectorizer = load_sentiment_model(caminho_modelo)
    dataset = pd.read_csv(caminho_csv, encoding='utf-8', low_memory=False, dtype=str)
    dataset['review_text'] = dataset['review_text'].fillna('')

    formatar_csv(caminho_csv)

    dataset_formatado = pd.read_csv("C:\\csv_formatado.csv", encoding='utf-8', low_memory=False, dtype=str)
    dataset_formatado['review_text'] = dataset_formatado['review_text'].fillna('')

    X = dataset_formatado['review_text'].values
    Y = dataset_formatado['feeling'].values

    X_ngrams = ngram_vectorizer.transform(X)
    Y_pred = xgboost.predict(X_ngrams)

    df_results = pd.DataFrame({'Feeling_Predicted': Y_pred, 'Feeling_True': Y})
    uniao = pd.concat([dataset, df_results], axis=1)

    processar_coluna(uniao, "submission_date")
    processar_coluna(uniao, "reviewer_id")
    processar_coluna(uniao, "product_id")
    processar_coluna(uniao, "product_name")
    processar_coluna(uniao, "site_category_lv1")
    processar_coluna(uniao, "site_category_lv2")
    processar_coluna(uniao, "review_title")
    processar_coluna(uniao, "recommend_to_a_friend")
    processar_coluna(uniao, "review_text")
    processar_coluna(uniao, "reviewer_gender")
    processar_coluna(uniao, "reviewer_state")

    mapping = {0: 'Negativo', 1: 'Neutro', 2: 'Positivo'}

    uniao['Feeling_Predicted'] = uniao['Feeling_Predicted'].replace(mapping)
    uniao['Feeling_Predicted'] = uniao['Feeling_Predicted'].fillna('')

    uniao['Feeling_True'] = uniao['Feeling_True'].replace(mapping)
    uniao['Feeling_True'] = uniao['Feeling_True'].fillna('')

    uniao.to_csv("C:\\csv_completo.csv", index=False, encoding='utf-8')

    os.remove("C:\\csv_formatado.csv")

    insert_csv_to_mongodb("C:\\csv_completo.csv")

    os.remove("C:\\csv_completo.csv")
