import joblib
from joblib import load
import pandas as pd

def load_sentiment_model():
    model_ngrams, ngram_vectorizer, df_values, df_values_count = load('D:\\Codigos\\Fatec\\api6\HEXTECH-API6sem\\api6-back\\machineLearning\\modelo_e_vetorizador.joblib')
    return model_ngrams, ngram_vectorizer, df_values, df_values_count
