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
        caminho_lower = caminho_arquivo.lower()
        if caminho_lower.endswith(('.csv', '.txt')):
            df = pd.read_csv(caminho_arquivo)
        elif caminho_lower.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(caminho_arquivo)
        else:
            raise ValueError("Formato de arquivo não suportado.")
            
        # Limpeza vetorizada nativa do Pandas (mais limpo e eficiente)
        df.columns = df.columns.astype(str).str.strip().str.replace('\n', ' ')
        return df

    def limpar_markdown_para_html(self, texto_markdown: str) -> str:
        # Limpeza e formatação de Markdown para tags HTML
        texto = re.sub(r'^#+\s*', '', texto_markdown, flags=re.MULTILINE)
        texto = re.sub(r'\*\*(SEÇÃO \d+.*?)\*\*', r'\1', texto, flags=re.IGNORECASE)
        texto = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', texto)
        
        # Isola o texto a partir da SEÇÃO 1, se existir
        idx = texto.find('SEÇÃO 1')
        texto = texto[idx:] if idx != -1 else texto

        html_saida = []
        in_list = False

        # Itera apenas sobre linhas que não estão vazias após o strip
        linhas_validas = [l.strip() for l in texto.split('\n') if l.strip()]

        for linha in linhas_validas:
            if linha.upper().startswith('SEÇÃO'):
                if in_list: 
                    html_saida.append('</ul>')
                    in_list = False
                html_saida.append(f'<h2 style="color: #3f51b5; margin-top: 30px; border-bottom: 2px solid #eee; padding-bottom: 5px;">{linha}</h2>')
            
            elif linha.startswith(('* ', '- ')):
                if not in_list:
                    html_saida.append('<ul style="margin-bottom: 15px; padding-left: 20px;">')
                    in_list = True
                html_saida.append(f'<li style="margin-bottom: 8px; line-height: 1.6;">{linha[2:].strip()}</li>')
            
            else:
                if in_list: 
                    html_saida.append('</ul>')
                    in_list = False
                html_saida.append(f'<p style="margin-bottom: 15px; line-height: 1.6; text-align: justify;">{linha}</p>')

        if in_list:
            html_saida.append('</ul>')

        return '\n'.join(html_saida)

    def gerar_perfil_pandas(self, df):
        """
        Delegação Híbrida: O Pandas gera as estatísticas globais e calcula 
        antecipadamente a média individual de CADA item. Isso fornece à IA 
        os dados exatos para responder a qualquer ranking solicitado pelo utilizador.
        """
        perfil = ["=== RESUMO ESTATÍSTICO MATEMÁTICO (Gerado pelo Python) ==="]
        
        colunas_numericas = df.select_dtypes(include=['number']).columns
        # Pré-filtra apenas as colunas de texto que são categorias válidas (entre 2 e 49 itens únicos)
        colunas_texto = [col for col in df.select_dtypes(include=['object', 'category']).columns if 1 < df[col].nunique() < 50]

        # 1. Estatísticas Globais
        if not colunas_numericas.empty:
            perfil.extend(["\n--- 1. ESTATÍSTICAS GERAIS ---", df.describe().to_string()])
        
        # 2. Contagem de Frequência
        if colunas_texto:
            perfil.append("\n--- 2. CONTAGEM DE FREQUÊNCIA ---")
            for col in colunas_texto:
                perfil.append(f"\nContagem para '{col}':\n{df[col].value_counts().to_string()}")

            # 3. Cardápio de Médias Agrupadas (Executado apenas se também houver números)
            if not colunas_numericas.empty:
                perfil.extend([
                    "\n--- 3. MÉDIAS EXATAS POR ITEM ---",
                    "ATENÇÃO IA: Use EXATAMENTE os valores desta lista abaixo para responder a solicitações sobre os melhores, piores ou notas de itens específicos."
                ])
                for col_texto in colunas_texto:
                    for col_num in colunas_numericas:
                        media_agrupada = df.groupby(col_texto)[col_num].mean().sort_values(ascending=False)
                        perfil.append(f"\nMédia de '{col_num}' agrupada por '{col_texto}':\n{media_agrupada.to_string()}")
                        
        return "\n".join(perfil)

    def analisar_dados(self, df, instrucao_usuario: str, instrucoes_extras: str = ""):
        info_dados = f"Dimensão Total: {df.shape[0]} linhas x {df.shape[1]} colunas."
        
        # Pré-processamento matemático e agrupamentos
        resumo_estatistico = self.gerar_perfil_pandas(df)
        
        # Base completa em formato CSV para a leitura da IA
        dados_completos = df.to_csv(index=False)

        prompt = construir_prompt_mestre(
            instrucao_usuario, info_dados, resumo_estatistico, dados_completos, instrucoes_extras
        )

        # Chamada à API (RNF02: Temperature = 0.1 garante respostas determinísticas)
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.1)
        )
        
        return self.limpar_markdown_para_html(response.text)