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

    dataset = dataset.fillna('')

    dataset['overall_rating'] = pd.to_numeric(dataset['overall_rating'], errors='coerce')
    dataset = dataset.dropna(subset=['overall_rating'])
    dataset['overall_rating'] = dataset['overall_rating'].astype(float)

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

    script_dir = os.path.dirname(os.path.abspath(__file__))
    formatted_csv_path = os.path.join(script_dir, "csv_formatado.csv")
    dataset.to_csv(formatted_csv_path, index=False, encoding='utf-8')

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
    xgboost, ngram_vectorizer = load(caminho_modelo)
    dataset = pd.read_csv(caminho_csv, encoding='utf-8', low_memory=False, dtype=str)
    dataset['review_text'] = dataset['review_text'].fillna('')

    formatar_csv(caminho_csv)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    formatted_csv_path = os.path.join(script_dir, "csv_formatado.csv")
    dataset_formatado = pd.read_csv(formatted_csv_path, encoding='utf-8', low_memory=False, dtype=str)
    dataset_formatado['review_text'] = dataset_formatado['review_text'].fillna('')

    X = dataset_formatado['review_text'].values
    Y = dataset_formatado['feeling'].values

    X_ngrams = ngram_vectorizer.transform(X)
    Y_pred = xgboost.predict(X_ngrams)

    df_results = pd.DataFrame({'Feeling_Predicted': Y_pred, 'Feeling_True': Y})
    uniao = pd.concat([dataset, df_results], axis=1)

    columns_to_process = [
        "submission_date", "reviewer_id", "product_id", "product_name", 
        "site_category_lv1", "site_category_lv2", "review_title", 
        "recommend_to_a_friend", "review_text", "reviewer_gender", "reviewer_state"
    ]

    for column in columns_to_process:
        processar_coluna(uniao, column)

    mapping = {0: 'Negativo', 1: 'Neutro', 2: 'Positivo'}

    uniao['Feeling_Predicted'] = uniao['Feeling_Predicted'].replace(mapping).fillna('')
    uniao['Feeling_True'] = uniao['Feeling_True'].replace(mapping).fillna('')

    complete_csv_path = os.path.join(script_dir, "csv_completo.csv")
    uniao.to_csv(complete_csv_path, index=False, encoding='utf-8')

    os.remove(formatted_csv_path)

    insert_csv_to_mongodb(complete_csv_path)

    os.remove(complete_csv_path)
