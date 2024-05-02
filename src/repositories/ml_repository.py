# Imports necessários
import re
import string
import unicodedata
import numpy as np
import pandas as pd
from joblib import load
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# carrega o modelo e vetorizador
def load_sentiment_model(caminho_modelo):
    #define modelo como "model_ngrams" e vetorizador como "ngram_vectorizer" e carrega de acordo local do seu arquivo
    model_ngrams, ngram_vectorizer = load(caminho_modelo)
    return model_ngrams, ngram_vectorizer

# formata o texto para melhorar resultado do modelo
def formatar_csv(caminho_csv):
    dataset = pd.read_csv(caminho_csv)

    # substitue espaços vazios por strings em branco
    dataset['review_text'] = dataset['review_text'].fillna('')

    # Cria uma coluna para arzenas sentimentos antes de serem passados no modelo
    dataset['feeling'] = np.where(dataset['overall_rating'] < 3, 'Negative', np.where(dataset['overall_rating'] == 3, 'Neutral', 'Positive'))

    # Pré-processamento dos dados
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('portuguese'))

    preprocessed_texts = []  # Lista para armazenar os textos pré-processados

    for text in dataset['review_text']:
        if isinstance(text, str):  # Verifica se o texto é uma string
            # Converter para minúsculas
            text = text.lower()
            # Remover acentos
            text = ''.join(char for char in unicodedata.normalize('NFKD', text) if unicodedata.category(char) != 'Mn')
            # Remover números usando expressão regular
            text = re.sub(r'\d+', '', text)
            # Remover caracteres especiais (incluindo emojis)
            text = re.sub(r'[^\w\s]', '', text)
            # Remover pontuação
            text = text.translate(str.maketrans('', '', string.punctuation))
            # Remover espaços extras
            text = re.sub(r'\s+', ' ', text).strip()
            # Tokenização
            tokens = word_tokenize(text)
            # Lematização e remoção de stopwords
            tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word.lower() not in stop_words]
            # Juntar tokens em texto novamente
            preprocessed_text = ' '.join(tokens)
            preprocessed_texts.append(preprocessed_text)  # Adicionar texto pré-processado à lista
        else:
            #pula linhas em branco sem alterar o tamnaho do csv
            preprocessed_texts.append("")

    # Atualiza o DataFrame com os textos pré-processados
    dataset['review_text'] = preprocessed_texts

    #cria o csv processado na raiz do disco c
    dataset.to_csv("C:\\csv_formatado.csv ", index=False)

    return dataset

def add_feelings(caminho_modelo, caminho_csv):
    # Carrega o modelo
    model_ngrams, ngram_vectorizer = load_sentiment_model(caminho_modelo)

    # Carrega o CSV
    dataset = pd.read_csv(caminho_csv)

    # substitue espaços vazios por strings em branco
    dataset['review_text'] = dataset['review_text'].fillna('')

    # Formata o CSV
    formatar_csv(caminho_csv)

    # Carrega o CSV formatado
    dataset_formatado = pd.read_csv("C:\\csv_formatado.csv")

    # substitue espaços vazios por strings em branco
    dataset_formatado['review_text'] = dataset_formatado['review_text'].fillna('')

    # Separa colunas a serem usadas pelo modelo.
    X = dataset_formatado['review_text'].values
    Y = dataset_formatado['feeling'].values

    # Vetorizar os dados de texto com N-grams
    X_ngrams = ngram_vectorizer.transform(X)

    # Prever as classes para os dados de teste
    Y_pred = model_ngrams.predict(X_ngrams)

    # Criar um DataFrame com as previsões e as verdadeiras classes de "feeling"
    df_results = pd.DataFrame({'Feeling_Predicted': Y_pred, 'Feeling_True': Y})

    # Adiciona as duas colunas geradas no fim do CSV original.
    uniao = pd.concat([dataset, df_results], axis=1)

    # Salva o CSV com resultado do ML
    uniao.to_csv("C:\\csv_completo.csv", index=False)

add_feelings(
    "C:\\Users\\augus\\Documents\\VsCode\\fatec\\api6\\HEXTECH-API6sem\\api6-back\\machineLearning\\modelo_e_vetorizador.joblib",
    "C:\\fatec\\B2W-Reviews01\\B2W-Reviews01.csv"
)
