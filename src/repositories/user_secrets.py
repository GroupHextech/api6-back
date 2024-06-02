from ..database.mongodb import get_user_secrets_collection

def get_user_secret(email):
    user_secrets_collection = get_user_secrets_collection()
    
    # Busca o segredo pelo email na coleção user_secrets
    user_secret = user_secrets_collection.find_one({"email": email})
    
    if user_secret:
        return user_secret.get("secret")  # Retorna o segredo se encontrado
    else:
        return None  # Retorna None se nenhum segredo encontrado

def save_user_secret(email, secret):
    user_secrets_collection = get_user_secrets_collection()
    
    # Atualiza ou insere um novo documento com o email e secret
    user_secrets_collection.update_one(
        {"email": email},
        {"$set": {"secret": secret}},
        upsert=True
    )