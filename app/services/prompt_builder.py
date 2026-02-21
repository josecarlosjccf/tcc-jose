import logging

# Configuração básica de log para registrar eventos e erros no terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def construir_prompt_mestre(
    instrucao_usuario: str, 
    info_dados: str, 
    resumo_estatistico: str, 
    dados_completos: str, 
    instrucoes_extras: str = ""
) -> str:
    """
    Constrói o prompt estruturado com validação de entradas e tratamento de erros.
    Garante que a IA não seja acionada com parâmetros essenciais vazios.
    """
    try:
        # =====================================================================
        # 1. VALIDAÇÃO DE ENTRADAS (Tratamento de Erros de Input)
        # =====================================================================
        
        # Impede a criação do prompt se não houver instrução do usuário
        if not instrucao_usuario or not instrucao_usuario.strip():
            raise ValueError("Erro Crítico: A instrução do usuário não pode estar vazia.")
            
        # Impede a criação do prompt se a planilha estiver vazia
        if not dados_completos or not dados_completos.strip():
            raise ValueError("Erro Crítico: Os dados da planilha não podem estar vazios.")
            
        # Se faltar info secundária, o sistema não cai, mas avisa no log do terminal
        if not info_dados:
            logging.warning("Aviso: 'info_dados' está vazio. O prompt será gerado sem a dimensão da base.")
            info_dados = "Dimensão da base não informada."
            
        if not resumo_estatistico:
            logging.warning("Aviso: 'resumo_estatistico' está vazio. A IA analisará sem os cálculos do Pandas.")
            resumo_estatistico = "Resumo estatístico prévio não disponível."

        # =====================================================================
        # 2. MONTAGEM SEGURA DO PROMPT
        # =====================================================================
        
        prompt = f"""
        **CONTEXTO E REGRAS DE SEGURANÇA:** Você é um Analista de Dados Profissional. 
        
        # REGRA MÁXIMA: 
        # Não faça cálculos matemáticos complexos de contagem ou médias. O sistema (Python/Pandas) já fez o processamento numérico exato e gerou um "Resumo Estatístico" abaixo. Use os números desse resumo estatístico como verdade absoluta. Foque sua inteligência em cruzar esses números com a "Base de Dados Completa" para gerar insights executivos e interpretar os textos/comentários.
        # NUNCA invente dados. Se a resposta não estiver nos dados, diga que não há informações suficientes.

        **ESTRUTURA DE SAÍDA OBRIGATÓRIA:** Retorne um texto em Markdown com 4 seções. Use negrito **texto** e listas - para clareza:

        SEÇÃO 1: RESUMO EXECUTIVO DOS DADOS
        SEÇÃO 2: PRINCIPAIS DESCOBERTAS E TENDÊNCIAS
        SEÇÃO 3: RESPOSTA AO PEDIDO DO USUÁRIO
        SEÇÃO 4: RECOMENDAÇÕES E PRÓXIMOS PASSOS

        **INFORMAÇÕES DA BASE:**
        {info_dados}

        **1. RESUMO ESTATÍSTICO (GERADO PELO PANDAS):**
        ```
        {resumo_estatistico}
        ```
        
        **2. BASE DE DADOS COMPLETA (PARA ANÁLISE QUALITATIVA/TEXTUAL):**
        ```csv
        {dados_completos}
        ```

        **INSTRUÇÃO DO USUÁRIO:**
        {instrucao_usuario}
        {instrucoes_extras}

        **IMPORTANTE:** Sua resposta DEVE começar IMEDIATAMENTE com 'SEÇÃO 1: RESUMO EXECUTIVO DOS DADOS'.
        """
        
        logging.info("Prompt mestre construído com sucesso e pronto para envio.")
        return prompt

    except ValueError as ve:
        # Captura erros de validação (ex: campos essenciais em branco)
        logging.error(f"Falha de Validação na construção do prompt: {ve}")
        raise
    except Exception as e:
        # Captura erros imprevistos (ex: falha de memória ao processar string gigante)
        logging.critical(f"Erro inesperado no Prompt Builder: {e}")
        raise RuntimeError(f"Falha interna ao gerar o prompt estruturado: {e}")