from flask import Flask

def criar_app():
    app = Flask(__name__)
    app.secret_key = 'tcc_jose_carlos_secreto_2026' 
    
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app