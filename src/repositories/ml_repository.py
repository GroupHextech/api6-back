import joblib


def load_sentiment_model(testes):
    filename = 'D:\\Codigos\\Fatec\\api6\\HEXTECH-API6sem\\api6-back\\machineLearning\\modelo_e_vetorizador.joblib'
    modelo_carregado, vetorizador_carregado = joblib.load(filename)
    
    freq_testes = vetorizador_carregado.transform(testes)
    previsoes = modelo_carregado.predict(freq_testes)

    return previsoes.tolist()