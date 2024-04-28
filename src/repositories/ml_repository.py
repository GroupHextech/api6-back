import joblib
from joblib import load
import pandas as pd

def load_sentiment_model():
    modelo_carregado, X_ngrams, df_results_true_count = load('D:\\Codigos\\Fatec\\api6\HEXTECH-API6sem\\api6-back\\machineLearning\\modelo_e_vetorizador.joblib')
    return modelo_carregado, X_ngrams, df_results_true_count
