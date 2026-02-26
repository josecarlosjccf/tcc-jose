import pandas as pd
import re
from google import genai
from google.genai import types  
from app.services.prompt_builder import construir_prompt_mestre

class DataAnalyzer:
    def __init__(self, api_key: str, versao_modelo: str):
        self.client = genai.Client(api_key=api_key)
        self.model_name = f'gemini-{versao_modelo}-flash'

    def carregar_planilha(self, caminho_arquivo: str) -> pd.DataFrame:
        extensao = caminho_arquivo.lower()
        if extensao.endswith(('.csv', '.txt')):
            df = pd.read_csv(caminho_arquivo)
        elif extensao.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(caminho_arquivo)
        else:
            raise ValueError("Formato de arquivo não suportado.")
            
        # Limpeza vetorizada nativa do Pandas
        df.columns = df.columns.astype(str).str.strip().str.replace('\n', ' ')
        return df

    def _formatar_linha_html(self, linha: str) -> str:
        """Função auxiliar para aplicar os estilos CSS diretos (Tailwind-like) nas tags."""
        if linha.upper().startswith('SEÇÃO'):
            return f'<h2 style="color: #3f51b5; margin-top: 30px; border-bottom: 2px solid #eee; padding-bottom: 5px;">{linha}</h2>'
        elif linha.startswith(('* ', '- ')):
            return f'<li style="margin-bottom: 8px; line-height: 1.6;">{linha[2:].strip()}</li>'
        return f'<p style="margin-bottom: 15px; line-height: 1.6; text-align: justify;">{linha}</p>'

    def limpar_markdown_para_html(self, texto_markdown: str) -> str:
        # Limpeza e substituição inicial de marcações
        texto = re.sub(r'^#+\s*', '', texto_markdown, flags=re.MULTILINE)
        texto = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', texto)
        
        # Garante que o texto comece a partir da SEÇÃO 1
        if 'SEÇÃO 1' in texto.upper():
            texto = texto[texto.upper().find('SEÇÃO 1'):]

        html_saida = []
        in_list = False

        # Itera apenas por linhas que contenham texto útil
        for linha in [l.strip() for l in texto.split('\n') if l.strip()]:
            eh_item_lista = linha.startswith(('* ', '- '))
            
            # Controle dinâmico de abertura e fechamento de listas (<ul>)
            if eh_item_lista and not in_list:
                html_saida.append('<ul style="margin-bottom: 15px; padding-left: 20px;">')
                in_list = True
            elif not eh_item_lista and in_list:
                html_saida.append('</ul>')
                in_list = False

            # Aplica a tag HTML via método auxiliar
            html_saida.append(self._formatar_linha_html(linha))

        if in_list:
            html_saida.append('</ul>')

        return '\n'.join(html_saida)

    def gerar_perfil_pandas(self, df: pd.DataFrame) -> str:
        """
        Delegação Híbrida: O Pandas pré-calcula as médias e contagens (motor matemático).
        Fornece os dados exatos à IA para rankings e análises, prevenindo alucinações.
        """
        perfil = ["=== RESUMO ESTATÍSTICO MATEMÁTICO (Gerado pelo Python) ==="]
        
        colunas_num = df.select_dtypes(include=['number']).columns
        # Filtra colunas de texto para categorias válidas (2 a 49 itens únicos)
        colunas_txt = [c for c in df.select_dtypes(include=['object', 'category']).columns if 1 < df[c].nunique() < 50]

        if not colunas_num.empty:
            perfil.extend(["\n--- 1. ESTATÍSTICAS GERAIS ---", df.describe().to_string()])
        
        if colunas_txt:
            perfil.append("\n--- 2. CONTAGEM DE FREQUÊNCIA ---")
            # Usa list comprehension para adicionar todas as contagens de forma direta
            perfil.extend([f"\nContagem para '{c}':\n{df[c].value_counts().to_string()}" for c in colunas_txt])

            # Cardápio de Médias Agrupadas (Executado apenas se houver colunas numéricas e de texto)
            if not colunas_num.empty:
                perfil.extend([
                    "\n--- 3. MÉDIAS EXATAS POR ITEM ---",
                    "ATENÇÃO IA: Use EXATAMENTE os valores abaixo para solicitações sobre itens específicos."
                ])
                for txt in colunas_txt:
                    for num in colunas_num:
                        media_agrupada = df.groupby(txt)[num].mean().sort_values(ascending=False)
                        perfil.append(f"\nMédia de '{num}' agrupada por '{txt}':\n{media_agrupada.to_string()}")
                        
        return "\n".join(perfil)

    def analisar_dados(self, df: pd.DataFrame, instrucao_usuario: str, instrucoes_extras: str = "") -> str:
        # Delegação Híbrida em ação: Matemática local (Pandas) + Semântica em nuvem (Gemini)
        resumo_estatistico = self.gerar_perfil_pandas(df)
        dados_completos = df.to_csv(index=False)
        info_dados = f"Dimensão Total: {df.shape[0]} linhas x {df.shape[1]} colunas."

        prompt = construir_prompt_mestre(
            instrucao_usuario, info_dados, resumo_estatistico, dados_completos, instrucoes_extras
        )

        # Chamada à API com Trava de Alucinação (RNF02: Temperature = 0.1)
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.1)
        )
        
        return self.limpar_markdown_para_html(response.text)