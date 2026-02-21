def construir_prompt_mestre(instrucao_usuario, info_dados, amostra_head, amostra_completa, instrucoes_extras=""):
    prompt = f"""
    **CONTEXTO:** Você é um Analista de Dados Profissional.

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

    **IMPORTANTE:** Sua resposta DEVE começar IMEDIATAMENTE com 'SEÇÃO 1: RESUMO EXECUTIVO DOS DADOS'.
    """
    return prompt