# Instala as bibliotecas necessárias (necessário apenas em ambientes como Google Colab)
!pip install -q google-genai pandas openpyxl

# Importa as bibliotecas
from google.colab import files
import pandas as pd
import os
import re
from google import genai
from google.genai import types

# --- CONFIGURAÇÕES DE ACESSO E ANÁLISE ---

# 🚨 1. CHAVE DE API DO GEMINI 🚨
GEMINI_API_KEY = "API-KEY-AQUI"

# 🛑 2. LOCAL EXCLUSIVO PARA O PROMPT DO USUÁRIO 🛑
# Escreva abaixo a instrução completa do que a IA deve analisar, buscando nos
# dados do arquivo CSV ou XLSX que você irá carregar.
USER_ANALYSIS_PROMPT = """
Faça a análise das respostas às questões e com base nisso descreva como precisaria ser essa ferramenta para os professores.
"""
# ----------------------------------------------------

# Constantes do Modelo e Saída
MODEL_NAME = 'gemini-2.5-flash'
OUTPUT_FILE_NAME = "relatorio_analise_personalizada.html"

class DataAnalyzer:
    """
    Classe para carregar dados (CSV/XLSX), analisar com a API Gemini
    e gerar um relatório HTML estruturado.
    """

    def __init__(self, api_key: str, model_name: str, output_file: str):
        # Inicialização do cliente da API
        if not api_key:
            raise ValueError("Chave de API do Gemini não fornecida.")
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.output_file = output_file
        self.df = None
        self.file_name = None

    def _load_data(self):
        """Carrega o arquivo CSV/XLSX do usuário."""
        print("Aguardando o upload do seu arquivo CSV/XLSX. Por favor, selecione o arquivo.")
        try:
            uploaded = files.upload()
            if not uploaded: return False

            self.file_name = list(uploaded.keys())[0]

            # Lógica para leitura universal (CSV ou XLSX)
            if self.file_name.lower().endswith(('.csv', '.txt')):
                self.df = pd.read_csv(self.file_name)
            elif self.file_name.lower().endswith(('.xlsx', '.xls')):
                self.df = pd.read_excel(self.file_name)
            else:
                print("\n❌ ERRO: Formato de arquivo não suportado.")
                return False

            # Normaliza nomes de colunas
            self.df.columns = [col.strip().replace('\n', ' ') for col in self.df.columns]
            print(f"\n✅ Arquivo '{self.file_name}' carregado e preparado.")
            return True

        except Exception as e:
            print(f"\n❌ ERRO ao carregar o arquivo: {e}")
            return False

    def _generate_master_prompt(self, user_instruction: str) -> str:
        """
        Cria o prompt com a estrutura de relatório obrigatória, injetando
        a amostra dos dados e a instrução do usuário.
        """

        # Amostra dos dados para a IA entender a estrutura
        data_head = self.df.head().to_markdown(index=False)
        data_info = f"Dimensão do DataSet: {self.df.shape[0]} linhas x {self.df.shape[1]} colunas."
        data_sample = self.df.to_string(index=False, max_rows=50)

        prompt = f"""
        **CONTEXTO:** Você é um Analista de Dados Profissional.

        **ESTRUTURA DE SAÍDA OBRIGATÓRIA:** Retorne um texto formatado em Markdown com as seguintes 4 seções. Use negrito **texto** e listas - para clareza:

        SEÇÃO 1: RESUMO EXECUTIVO DOS DADOS
        SEÇÃO 2: PRINCIPAIS DESCOBERTAS E TENDÊNCIAS
        SEÇÃO 3: RESPOSTA AO PEDIDO DO USUÁRIO
        SEÇÃO 4: RECOMENDAÇÕES E PRÓXIMOS PASSOS

        **DADOS BRUTOS ANALISADOS:**
        {data_info}
        Amostra e Estrutura das Primeiras Linhas:
        ```
        {data_head}
        ```
        Conteúdo Completo (Amostra):
        ```
        {data_sample}
        ```

        **INSTRUÇÃO DO USUÁRIO:**
        {user_instruction}

        **IMPORTANTE:** Sua resposta DEVE começar IMEDIATAMENTE com 'SEÇÃO 1: RESUMO EXECUTIVO DOS DADOS' e seguir a estrutura de 4 seções, SEM TEXTO DE INTRODUÇÃO ou PREÂMBULO antes da primeira seção.
        """
        return prompt

    def _text_to_html_body(self, text: str) -> str:
        """
        Converte o texto do Gemini (Markdown) para HTML formatado com Tailwind.
        Ajustes para limpeza de tags expostas e correção da numeração de seção.
        """

        h2_style = 'text-2xl font-bold mt-8 mb-4 text-indigo-700 border-b-2 border-indigo-200 pb-2'
        # Adicionado 'text-justify' aqui e em p_style
        li_style = 'text-gray-700 leading-relaxed mb-1 ml-6 list-disc text-justify'
        p_style = 'text-gray-700 leading-relaxed mb-4 text-justify'

        html_content = text

        # 1. Limpeza Crítica: Elimina qualquer texto antes da SEÇÃO 1 e corrige a estrutura
        match_start = re.search(r'(SEÇÃO 1: .*?)', html_content, re.DOTALL)
        if match_start:
            html_content = html_content[match_start.start():]
        else:
            return f'<p class="{p_style} text-red-600 font-bold">⚠️ Erro de Formatação: A IA não seguiu a estrutura. Conteúdo bruto:<br>{html_content}</p>'


        # 2. Conversão e Correção dos Cabeçalhos de Seção (Resolve tags expostas e símbolos)
        # O regex garante que o número e o título sejam capturados corretamente.
        html_content = re.sub(
            r'SEÇÃO (\d+):\s*(.*)',
            r'</section><section class="mb-8"><h2 class="'+h2_style+r'">SEÇÃO \1: \2</h2>',
            html_content
        )

        # Inicia a primeira tag <section> de forma limpa
        html_content = '<section class="mb-8">' + html_content.lstrip('</section>')


        # 3. Converte negrito **texto**
        html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)

        # 4. Converte blocos de código (```...```)
        html_content = re.sub(r'```(.*?)```', r'<pre class="bg-gray-100 p-3 rounded-lg overflow-x-auto my-4 text-sm whitespace-pre-wrap"><code>\1</code></pre>', html_content, flags=re.DOTALL)

        # 5. Converte itens de lista
        def convert_lists(match):
            lines = match.group(0).split('\n')
            list_html = '<ul class="mb-4 pl-4">'
            for line in lines:
                # O item de lista herda o estilo 'text-justify'
                item_content = re.sub(r'^[\s*-]\s*', '', line).strip()
                if item_content:
                    list_html += f'<li class="{li_style}">{item_content}</li>'
            list_html += '</ul>'
            return list_html
        html_content = re.sub(r'([\r\n]+)(?:[-\*]\s+.*(?:[\r\n]+|$))+', convert_lists, '\n' + html_content + '\n', flags=re.MULTILINE)

        # 6. Converte quebras de linha duplas em parágrafos <p> (com justificativa)
        html_content = html_content.strip().replace('\r', '')
        html_content_blocks = html_content.split('\n\n')
        final_blocks = []
        for block in html_content_blocks:
            block = block.strip()
            if not block: continue
            if re.match(r'<(ul|pre|h2|h3|table)', block, re.IGNORECASE):
                final_blocks.append(block)
            else:
                text_with_br = block.replace('\n', '<br>')
                # Parágrafo com 'text-justify'
                final_blocks.append(f'<p class="{p_style}">{text_with_br}</p>')

        html_content = '\n'.join(final_blocks)
        html_content = re.sub(r'</section><section class="mb-8">', '', html_content, 1) # Limpeza final

        return html_content

    def _generate_html_file(self, html_body_content: str):
        """Cria e salva o arquivo HTML final."""

        html_template = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Relatório de Análise de Dados</title>
            <!-- Carregamento do Tailwind CSS CDN -->
            <script src="https://cdn.tailwindcss.com"></script>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
                body {{ font-family: 'Inter', sans-serif; background-color: #f7f9fb; }}
                .report-container {{ box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); }}
                /* Garante que o texto seja justificado dentro do main content */
                #report-content p, #report-content li {{ text-align: justify; }}
            </style>
        </head>
        <body class="p-4 sm:p-8 md:p-12">
            <div class="max-w-5xl mx-auto bg-white rounded-xl report-container p-6 sm:p-10 md:p-12">
                <header class="mb-10 border-b-4 border-indigo-500 pb-4">
                    <h1 class="text-4xl font-extrabold text-gray-900 leading-tight">Relatório de Análise Personalizada</h1>
                    <p class="text-lg text-indigo-500 mt-2">Análise de IA para o arquivo '{self.file_name}'</p>
                </header>

                <main id="report-content">
                    {html_body_content}
                </main>
            </div>
        </body>
        </html>
        """
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(html_template)

    def analyze_and_report(self, user_instruction: str):
        """Método principal que coordena o fluxo de trabalho."""

        # 1. Carregamento dos dados
        if not self._load_data():
            return

        # 2. Geração do prompt mestre
        print("Preparando dados e gerando prompt para a IA...")
        prompt_mestre = self._generate_master_prompt(user_instruction)

        # 3. Chamada à API
        print("Iniciando a geração do Relatório de Análise com a IA...")
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt_mestre
            )
            relatorio_final = response.text
        except Exception as e:
            relatorio_final = f"❌ ERRO GRAVE NA API: Não foi possível gerar o relatório. Detalhes: {e}"
            print(relatorio_final)
            return

        # 4. Conversão e salvamento do HTML
        html_body_content = self._text_to_html_body(relatorio_final)
        self._generate_html_file(html_body_content)

        print("\n" + "="*70)
        print("✅ ANÁLISE CONCLUÍDA! O Relatório de Análise foi gerado em formato HTML.")
        print(f"O resultado foi salvo em: {self.output_file}")
        print("======================================================================")

# --- Execução Principal ---
if __name__ == "__main__":
    if not GEMINI_API_KEY:
        print("⚠️ ERRO: Por favor, insira sua chave de API do Gemini no código.")
    else:
        analyzer = DataAnalyzer(
            api_key=GEMINI_API_KEY,
            model_name=MODEL_NAME,
            output_file=OUTPUT_FILE_NAME
        )
        analyzer.analyze_and_report(USER_ANALYSIS_PROMPT)
