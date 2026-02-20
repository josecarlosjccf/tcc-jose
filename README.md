# PYTHON E GEMINI: ANÁLISE DE PLANILHAS COM IA GENERATIVA

Repositório destinado ao Trabalho de Conclusão de Curso (TCC) de Sistemas de Informação - 2026.
Autor: José Carlos Cândido Ferreira.

## Estrutura do Projeto

O projeto adota uma arquitetura modular para facilitar a manutenção e escalabilidade:

- **`app/`**: Contém todo o código-fonte da aplicação web.
  - **`main.py`**: Arquivo principal que inicia o servidor e define as rotas da API.
  - **`services/`**: Camada de regras de negócio. O arquivo `data_analyzer.py` contém a lógica de Data Wrangling com Pandas e a comunicação com a API do Google Gemini.
  - **`templates/`**: Arquivos HTML renderizados para o usuário final.
  - **`static/`**: Arquivos estáticos (CSS, imagens, JavaScript do lado do cliente).
- **`uploads/`**: Diretório temporário para armazenamento das planilhas (`.csv`, `.xlsx`) enviadas pelos usuários.
- **`outputs/`**: Diretório onde os relatórios analíticos estruturados em HTML são salvos após a inferência da IA.
- **`.env`**: Arquivo de configuração de variáveis de ambiente (chaves de API). Não versionado.