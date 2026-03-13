import os
from dotenv import load_dotenv
from app import criar_app

load_dotenv()

app = criar_app()

if __name__ == '__main__':
    # Configurações dinâmicas baseadas no ambiente (.env)
    modo_debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    porta = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '127.0.0.1')

    app.run(host=host, port=porta, debug=modo_debug)