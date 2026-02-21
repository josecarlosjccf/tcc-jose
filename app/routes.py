import os
from flask import Blueprint, render_template, request
from app.services.data_analyzer import DataAnalyzer
from dotenv import load_dotenv

load_dotenv()
CHAVE_API = os.getenv("GEMINI_API_KEY")
VERSAO_GEMINI = os.getenv("GEMINI_VERSION", "2.5")

main_bp = Blueprint('main', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@main_bp.route('/', methods=['GET'])
def index():
    # Carrega a página inicial (upload)
    return render_template('index.html')

@main_bp.route('/analisar', methods=['POST'])
def analisar():
    # Pega o arquivo e a instrução enviados pelo usuário
    arquivo = request.files.get('file')
    prompt_usuario = request.form.get('prompt')

    if not arquivo or arquivo.filename == '':
        return "Erro: Nenhum arquivo enviado.", 400

    # Salva o arquivo na pasta /uploads
    caminho_arquivo = os.path.join(UPLOAD_FOLDER, arquivo.filename)
    arquivo.save(caminho_arquivo)

    try:
        # Envia para o Gemini processar
        analisador = DataAnalyzer(api_key=CHAVE_API, versao_modelo=VERSAO_GEMINI)
        df = analisador.carregar_planilha(caminho_arquivo)
        
        html_gerado = analisador.analisar_dados(df, prompt_usuario)
        
        # Devolve a segunda página preenchida
        return render_template('resultado.html', conteudo_relatorio=html_gerado)
        
    except Exception as e:
        return f"Erro ao processar a IA: {str(e)}", 500