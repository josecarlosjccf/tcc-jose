# PYTHON E GEMINI: ANÁLISE DE PLANILHAS COM IA GENERATIVA

**Trabalho de Conclusão de Curso (TCC)** **Curso:** Bacharelado em Sistemas de Informação - 2026  
**Autor:** José Carlos Cândido Ferreira  

---

## 💻 Sobre o Projeto

Este protótipo é um sistema web desenvolvido em Python (framework Flask) projetado para otimizar o fluxo de *reporting* na gestão de produtos e serviços. O sistema resolve o desafio da interpretação manual de grandes conjuntos de dados textuais não estruturados (como feedbacks, avaliações e respostas de formulários).

Através da integração do **Pandas** (para pré-processamento e manipulação de planilhas) com a **API do Google Gemini** (Inteligência Artificial Generativa), a ferramenta lê arquivos `.csv` e `.xlsx`, aplica técnicas de Engenharia de Prompt para mitigar alucinações da IA e devolve um relatório analítico estruturado diretamente em uma interface HTML.

---

## 🗂️ Arquitetura e Mapa de Pastas

O projeto adota a separação de responsabilidades (MVC adaptado), dividindo rotas, regras de negócio e interface visual:

```text
tcc-jose/
├── run.py                    # Arquivo principal que inicializa o servidor web.
├── .env                      # Arquivo (NÃO VERSIONADO) com as chaves de API.
├── requirements.txt          # Lista de dependências e versões exatas.
├── README.md                 # Documentação do projeto.
│
└── app/                      # Módulo central da aplicação Flask.
    ├── __init__.py           # Inicialização do Flask e segurança de sessões.
    ├── routes.py             # Controlador (Controller): gerencia as rotas web.
    │
    ├── services/             # Regras de Negócio (Services).
    │   ├── data_analyzer.py  # Ingestão do Pandas e comunicação com o Gemini.
    │   └── prompt_builder.py # Isolamento das estruturas de prompt e seções.
    │
    ├── templates/            # Interfaces de Usuário (Views - HTML).
    │   ├── index.html        # Página principal (Upload e Chat).
    │   ├── resultado.html    # Página do relatório processado pela IA.
    │   └── configuracoes.html# Painel para injeção de regras extras na IA.
    │
    └── static/               # Arquivos estáticos.
        └── css/
            └── style.css     # Folha de estilos padronizada.



O .env deve seguir o padrão:

GEMINI_API_KEY="SUA-CHAVE AQUI"
GEMINI_VERSION="2.5"