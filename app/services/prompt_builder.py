def construir_prompt_mestre(instrucao_usuario, info_dados, amostra_head, amostra_completa, instrucoes_extras=""):
    """
    Constrói o prompt estruturado que será enviado ao Gemini.
    Separa a formatação das regras de negócio e aplica as travas de segurança.
    """
    
    prompt = f"""
    **CONTEXTO E REGRAS DE SEGURANÇA (GROUNDING):** Você é um Analista de Dados Profissional. 
    
    # IMPORTANTE: A regra abaixo é a trava de ancoragem (Grounding). 
    # Ela proíbe a IA de inventar dados (alucinar) e a obriga a usar apenas o que o Pandas leu.
    REGRA MÁXIMA: Baseie-se EXCLUSIVAMENTE nos dados fornecidos abaixo. NUNCA invente nomes, números, métricas ou informações que não estejam na amostra. Se a resposta para a instrução do usuário não estiver nos dados, declare explicitamente: "Não há dados suficientes na planilha para responder a esta questão".

    # IMPORTANTE: Forçar essa estrutura de 4 seções tira a liberdade criativa da IA
    # e garante que o relatório sempre saia no mesmo padrão para o nosso HTML.
    **ESTRUTURA DE SAÍDA OBRIGATÓRIA:** Retorne um texto formatado em Markdown com as seguintes 4 seções. Use negrito **texto** e listas - para clareza:

    SEÇÃO 1: RESUMO EXECUTIVO DOS DADOS
    SEÇÃO 2: PRINCIPAIS DESCOBERTAS E TENDÊNCIAS
    SEÇÃO 3: RESPOSTA AO PEDIDO DO USUÁRIO
    SEÇÃO 4: RECOMENDAÇÕES E PRÓXIMOS PASSOS

    **INSTRUÇÕES DE CORREÇÃO E REGRAS EXTRAS:**
    {instrucoes_extras}

    **DADOS BRUTOS ANALISADOS:**
    {info_dados}
    
    Amostra e Estrutura das Primeiras Linhas:
    ```
    {amostra_head}
    ```
    
    Conteúdo Completo (Amostra):
    ```
    {amostra_completa}
    ```

    **INSTRUÇÃO DO USUÁRIO:**
    {instrucao_usuario}

    **IMPORTANTE:** Sua resposta DEVE começar IMEDIATAMENTE com 'SEÇÃO 1: RESUMO EXECUTIVO DOS DADOS' e seguir a estrutura de 4 seções, SEM TEXTO DE INTRODUÇÃO ou PREÂMBULO antes da primeira seção.
    """
    return prompt