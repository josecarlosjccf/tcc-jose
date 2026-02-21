import pandas as pd
import re
from google import genai
from app.services.prompt_builder import construir_prompt_mestre

class DataAnalyzer:
    def __init__(self, api_key: str, versao_modelo: str):
        self.client = genai.Client(api_key=api_key)
        self.model_name = f'gemini-{versao_modelo}-flash'

    def carregar_planilha(self, caminho_arquivo: str):
        if caminho_arquivo.lower().endswith(('.csv', '.txt')):
            df = pd.read_csv(caminho_arquivo)
        elif caminho_arquivo.lower().endswith(('.xlsx', '.xls')):
            df = pd.read_excel(caminho_arquivo)
        else:
            raise ValueError("Formato de arquivo não suportado.")
            
        df.columns = [str(col).strip().replace('\n', ' ') for col in df.columns]
        return df

    def limpar_markdown_para_html(self, texto_markdown: str) -> str:
        match_start = re.search(r'(SEÇÃO 1: .*?)', texto_markdown, re.DOTALL)
        html = texto_markdown[match_start.start():] if match_start else texto_markdown
            
        html = re.sub(r'SEÇÃO (\d+):\s*(.*)', r'<h2>SEÇÃO \1: \2</h2>', html)
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        
        blocos = html.strip().split('\n\n')
        blocos_finais = []
        for bloco in blocos:
            if not bloco.startswith('<h2'):
                bloco = f"<p>{bloco.replace('\n', '<br>')}</p>"
            blocos_finais.append(bloco)
            
        return '\n'.join(blocos_finais)

    def analisar_dados(self, df, instrucao_usuario: str, instrucoes_extras: str = ""):
        amostra_head = df.head().to_markdown(index=False)
        info_dados = f"Dimensão: {df.shape[0]} linhas x {df.shape[1]} colunas."
        amostra_completa = df.to_string(index=False, max_rows=50)

        prompt = construir_prompt_mestre(
            instrucao_usuario, info_dados, amostra_head, amostra_completa, instrucoes_extras
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        
        return self.limpar_markdown_para_html(response.text)