from flask import Flask, request, redirect, url_for, jsonify, session, render_template_string
from flask_cors import CORS
from .routes import blueprint_review, blueprint_blacklist, blueprint_fbusers, blueprint_clients, bp_generate, bp_verify
from .database import mongodb, firebase
from dotenv import load_dotenv

from authlib.integrations.flask_oauth2 import AuthorizationServer, ResourceProtector
from authlib.oauth2.rfc7662 import IntrospectionEndpoint
from authlib.oauth2.rfc6750 import BearerTokenValidator

from .repositories import client_repository, token_repository, user_repository
from .Auth import AuthorizationCodeGrant, MyJWTBearerToken
import jwt

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

authorization = AuthorizationServer(app)

# Desativando a validação HTTPS para desenvolvimento
app.config['OAUTH2_REQUIRE_HTTPS'] = False
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

authorization.register_grant(AuthorizationCodeGrant)

jwt_bearer_token = MyJWTBearerToken
authorization.register_token_generator('authorization_code', MyJWTBearerToken)

# require_oauth = ResourceProtector()
# class MyBearerTokenValidator(BearerTokenValidator):
#     def __init__(self, secret_key, algorithm='HS256'):
#         self.secret_key = secret_key
#         self.algorithm = algorithm

#     def authenticate_token(self, token_string):
#         try:
#             token = jwt.decode(token_string, self.secret_key, algorithms=[self.algorithm])
#             return token_repository.get(token_string)
#         except jwt.ExpiredSignatureError:
#             return None

# require_oauth.register_token_validator(MyBearerTokenValidator)

@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    if request.method == 'GET':
        client_id = request.args.get('client_id')
        client = client_repository.get(client_id)
        if not client:
            return 'Client not found', 404

        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Authorize</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        background-color: #f7f7f7;
                    }
                    .container {
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        width: 300px;
                    }
                    .form-group {
                        margin-bottom: 15px;
                    }
                    label {
                        display: block;
                        margin-bottom: 5px;
                    }
                    input[type="text"], input[type="password"] {
                        width: 100%;
                        padding: 8px;
                        box-sizing: border-box;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                    }
                    button {
                        width: 100%;
                        padding: 10px;
                        background-color: #28a745;
                        border: none;
                        border-radius: 4px;
                        color: #fff;
                        font-size: 16px;
                        cursor: pointer;
                    }
                    button:hover {
                        background-color: #218838;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <form method="post">
                        <input type="hidden" name="client_id" value="{{ client_id }}">
                        <input type="hidden" name="redirect_uri" value="{{ redirect_uri }}">
                        <input type="hidden" name="scope" value="{{ scope }}">
                        <input type="hidden" name="response_type" value="{{ response_type }}">
                        
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input type="text" id="username" name="username" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Password</label>
                            <input type="password" id="password" name="password" required>
                        </div>
                        <button type="submit">Sign in</button>
                    </form>
                </div>
            </body>
            </html>
        ''', client_id=client_id, redirect_uri=request.args.get('redirect_uri'), scope=request.args.get('scope'), response_type=request.args.get('response_type'))

    if request.method == 'POST':
        client_id = request.form['client_id']
        redirect_uri = request.form['redirect_uri']
        scope = request.form['scope']
        response_type = request.form['response_type']
        username = request.form['username']
        password = request.form['password']

        user_data = user_repository.authenticate_user(username, password)
        if user_data:
            print('user logged in successfully')
            session['user_id'] = str(user_data['_id'])  # Salvando o ID do usuário na sessão
            grant_user = user_data
            # grant = authorization.generate_access_token(grant_type=response_type,
            #                                             client_id=client_id,
            #                                             user=grant_user,
            #                                             scope=scope)

            grant = authorization.create_authorization_response(grant_user=grant_user)
            
            # Constrói a URL de redirecionamento com os parâmetros do grant token
            redirect_uri = request.form['redirect_uri']
            redirect_url = redirect_uri + '?access_token=' + grant['access_token'] + '&token_type=Bearer' + '&expires_in=' + grant['expires_in'] + '&scope=' + grant['scope']

            # Redireciona para a página especificada pelo redirect_uri
            return redirect(redirect_url)

        return 'Authentication failed', 401

@app.route('/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()

@app.route('/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_endpoint_response(IntrospectionEndpoint)


# MongoDB configuration
app.config["MONGO_URI"] = "mongodb+srv://admin:1234@api6.u8duoyj.mongodb.net/develop?ssl=true&retryWrites=true&w=majority&appName=Api6"
CORS(app)

# Inicia o Mongo
mongodb.init_db(app)

# Register blueprint
app.register_blueprint(blueprint_review)
app.register_blueprint(blueprint_blacklist)
app.register_blueprint(blueprint_fbusers)
app.register_blueprint(blueprint_clients)
app.register_blueprint(bp_generate)
app.register_blueprint(bp_verify)

# Inicia o Firebase
firebase.init_firestore()

if __name__ == "__main__":
    app.run()
