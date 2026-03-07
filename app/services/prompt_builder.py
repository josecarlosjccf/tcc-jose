import logging
from textwrap import dedent

# Configuração básica de log para registrar eventos no terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def construir_prompt_mestre(
    instrucao_usuario: str, 
    info_dados: str, 
    resumo_estatistico: str, 
    dados_completos: str, 
    instrucoes_extras: str = ""
) -> str:
    """
    Constrói o prompt estruturado aplicando as regras de segurança (RNF02).
    Garante que a IA receba os dados mínimos para não inventar informações.
    """
    try:
        # =====================================================================
        # 1. VALIDAÇÃO DE ENTRADAS ESSENCIAIS
        # =====================================================================
        if not instrucao_usuario or not instrucao_usuario.strip():
            raise ValueError("Erro Crítico: A instrução do usuário não pode estar vazia.")
            
        if not dados_completos or not dados_completos.strip():
            raise ValueError("Erro Crítico: Os dados da planilha não podem estar vazios.")
            
        # Fallback para dados secundários (evita que o sistema caia por detalhes)
        if not info_dados:
            logging.warning("Aviso: 'info_dados' ausente. Usando valor padrão.")
            info_dados = "Dimensão da base não informada."
            
        if not resumo_estatistico:
            logging.warning("Aviso: 'resumo_estatistico' ausente. Analisando sem cálculos prévios.")
            resumo_estatistico = "Resumo estatístico não disponível."

        # =====================================================================
        # 2. MONTAGEM SEGURA DO PROMPT
        # =====================================================================
        prompt = f"""
        **CONTEXTO E REGRAS DE SEGURANÇA:** Você é um Analista de Dados Profissional. 
        
        # REGRA MÁXIMA (PREVENÇÃO DE ALUCINAÇÕES): 
        # Não faça cálculos matemáticos de contagem ou médias. O sistema (Python/Pandas) já processou os números exatos e gerou o "Resumo Estatístico" abaixo. 
        # Use esses números como verdade absoluta. Foque sua inteligência em cruzar os números com os textos da "Base de Dados Completa" para gerar insights executivos.
        # NUNCA invente dados. Se a resposta não estiver no arquivo, diga que não há informações suficientes.

        **ESTRUTURA DE SAÍDA OBRIGATÓRIA:** (Retorne em Markdown, usando negrito e listas):
        SEÇÃO 1: RESUMO EXECUTIVO DOS DADOS
        SEÇÃO 2: PRINCIPAIS DESCOBERTAS E TENDÊNCIAS
        SEÇÃO 3: RESPOSTA AO PEDIDO DO USUÁRIO
        SEÇÃO 4: RECOMENDAÇÕES E PRÓXIMOS PASSOS

        **INFORMAÇÕES DA BASE:**
        {info_dados}

        **1. RESUMO ESTATÍSTICO (GERADO PELO PANDAS):**
        ```text
        {resumo_estatistico}
        ```
        
        **2. BASE DE DADOS COMPLETA (PARA ANÁLISE QUALITATIVA):**
        ```csv
        {dados_completos}
        ```

        **INSTRUÇÃO DO USUÁRIO:**
        {instrucao_usuario}
        {instrucoes_extras}

        **IMPORTANTE:** Sua resposta DEVE começar IMEDIATAMENTE com 'SEÇÃO 1: RESUMO EXECUTIVO DOS DADOS'.
        """
        
        logging.info("Prompt mestre construído com sucesso.")
        
        # O 'dedent' remove os recuos desnecessários do código, economizando tokens na API
        return dedent(prompt).strip()

    except ValueError as ve:
        logging.error(f"Falha de Validação no prompt: {ve}")
        raise
    except Exception as e:
        logging.critical(f"Erro inesperado no Prompt Builder: {e}")
        raise RuntimeError(f"Falha interna ao gerar o prompt estruturado: {e}")