from app import create_app

# Criar uma instância do aplicativo Flask
app = create_app()

if __name__ == '__main__':
    # Iniciar o servidor Flask
    app.run(debug=True)
