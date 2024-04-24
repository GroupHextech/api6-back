import joblib

model_path = "D:\Codigos\Fatec\api6\HEXTECH-API6sem\api6-back\machineLearning\modelo_e_vetorizador.joblib"

def load_sentiment_model(model_path):
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        print("Arquivo de modelo não encontrado.")
        return None
