import pandas as pd
import re
from google import genai
from google.genai import types  
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
        texto = re.sub(r'^#+\s*', '', texto_markdown, flags=re.MULTILINE)
        texto = re.sub(r'\*\*(SEÇÃO \d+.*?)\*\*', r'\1', texto, flags=re.IGNORECASE)
        texto = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', texto)
        
        idx = texto.find('SEÇÃO 1')
        if idx != -1:
            texto = texto[idx:]

        linhas = texto.split('\n')
        html_saida = []
        in_list = False

        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue

            if linha.upper().startswith('SEÇÃO'):
                if in_list:
                    html_saida.append('</ul>')
                    in_list = False
                html_saida.append(f'<h2 style="color: #2c3e50; margin-top: 30px; border-bottom: 2px solid #eee; padding-bottom: 5px;">{linha}</h2>')
            
            elif linha.startswith('* ') or linha.startswith('- '):
                if not in_list:
                    html_saida.append('<ul style="margin-bottom: 15px; padding-left: 20px;">')
                    in_list = True
                item_texto = linha[2:].strip()
                html_saida.append(f'<li style="margin-bottom: 8px; line-height: 1.6;">{item_texto}</li>')
            
            else:
                if in_list:
                    html_saida.append('</ul>')
                    in_list = False
                html_saida.append(f'<p style="margin-bottom: 15px; line-height: 1.6;">{linha}</p>')

        if in_list:
            html_saida.append('</ul>')

        return '\n'.join(html_saida)

    def gerar_perfil_pandas(self, df):
        # Motor Pandas: Gera as estatísticas matemáticas e contagens exatas
        perfil = ["=== RESUMO ESTATÍSTICO MATEMÁTICO (Gerado pelo Python) ==="]
        
        # Só gera o describe se existirem colunas numéricas
        colunas_numericas = df.select_dtypes(include=['number']).columns
        if not colunas_numericas.empty:
            perfil.append(df.describe().to_csv())
        
        perfil.append("\n=== TOP 5 VALORES MAIS FREQUENTES (Colunas Categóricas/Texto) ===")
        colunas_texto = df.select_dtypes(include=['object', 'category']).columns
        for col in colunas_texto:
            top_valores = df[col].value_counts().head(5)
            perfil.append(f"\nColuna '{col}':\n{top_valores.to_string()}")
            
        return "\n".join(perfil)

    def analisar_dados(self, df, instrucao_usuario: str, instrucoes_extras: str = ""):
        info_dados = f"Dimensão Total: {df.shape[0]} linhas x {df.shape[1]} colunas."
        
        # 1. Pré-processamento exato com Pandas
        resumo_estatistico = self.gerar_perfil_pandas(df)
        
        # 2. Base de dados completa para a IA ler TODOS os comentários sem pular nenhum
        dados_completos = df.to_csv(index=False)

        # Monta o prompt
        prompt = construir_prompt_mestre(
            instrucao_usuario, info_dados, resumo_estatistico, dados_completos, instrucoes_extras
        )

        # 3. Chama a IA com a trava de segurança contra alucinações (temperature=0.1)
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1  
            )
        )
        
        return self.limpar_markdown_para_html(response.text)