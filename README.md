# 📊 Analisador de Dados Python/Gemini

**Trabalho de Conclusão de Curso (TCC)** – Bacharelado em Sistemas de Informação (2026)  
**Autor:** José Carlos Cândido Ferreira  

<div align="center">

  <a href="https://www.python.org/" target="_blank">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>

  <a href="https://flask.palletsprojects.com/" target="_blank">
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  </a>

  <a href="https://pandas.pydata.org/" target="_blank">
    <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  </a>

  <a href="https://ai.google.dev/" target="_blank">
    <img src="https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white" alt="Gemini">
  </a>

  <a href="https://developer.mozilla.org/pt-BR/docs/Web/HTML" target="_blank">
    <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  </a>

  <a href="https://tailwindcss.com/" target="_blank">
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS">
  </a>

</div>

<br>

<div align="center">
  <img src="interface.png" alt="Interface do Analisador de Dados" width="800px" style="border-radius: 8px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);">
</div>

---

## 💻 Sobre o Projeto

Este protótipo é uma aplicação web desenvolvida em **Python (Flask)** projetada para otimizar o fluxo de *reporting* e análise na gestão de produtos e serviços.

O sistema resolve o desafio da interpretação manual de grandes conjuntos de dados textuais não estruturados, como feedbacks, avaliações e comentários qualitativos.

Através da integração do **Pandas** (para pré-processamento e manipulação de planilhas) com a **API do Google Gemini** (Inteligência Artificial Generativa), a ferramenta lê arquivos `.csv` e `.xlsx`, aplica técnicas rigorosas de Engenharia de Prompt e devolve um relatório analítico estruturado diretamente em uma interface HTML.

---

## 🛡️ Diferencial Técnico: Mitigação de Alucinações

O código foi arquitetado com travas de segurança rigorosas (RNF02) para garantir que a IA atue de forma puramente analítica e factual.

O sistema utiliza:

1. **Grounding (Ancoragem):** Instruções no prompt que proíbem a invenção de dados.  
2. **Contexto Integral:** Uso da função `to_csv(index=False)` no Pandas para injetar 100% dos dados na memória da IA, evitando cortes na leitura de planilhas extensas.  
3. **Hiperparâmetros Determinísticos:** Chamada da API configurada com `temperature=0.1`, reduzindo drasticamente a criatividade da rede neural e aumentando a previsibilidade das respostas.

---

## 🗂️ Arquitetura de Pastas

O projeto adota o padrão de separação de responsabilidades (MVC adaptado), dividindo rotas, regras de negócio e interfaces visuais:

```text
tcc-jose/
│
├── run.py                 # Inicializa o servidor web
├── .env                   # Variáveis de ambiente (Chave da API)
├── requirements.txt       # Dependências do projeto
├── README.md              # Documentação oficial
├── interface.png          # Print da tela principal
│
└── app/
    ├── __init__.py
    ├── routes.py
    │
    ├── services/
    │   ├── __init__.py
    │   ├── data_analyzer.py
    │   └── prompt_builder.py
    │
    ├── templates/
    │   ├── index.html
    │   └── resultado.html
    │
    └── static/
        └── css/
            └── style.css
```

---

## 🚀 Como Configurar e Rodar o Projeto

### ✅ 1. Clonar o Repositório

```bash
git clone https://github.com/josecarlosjccf/tcc-jose.git
cd tcc-jose
```

---

### ✅ 2. Pré-requisitos

Instale o **Python 3.12.9** ou superior.

---

### 📦 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

---

### 🔐 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
GEMINI_API_KEY="COLE_AQUI_A_SUA_CHAVE_GERADA"
GEMINI_VERSION="2.5"
```

⚠️ O `.env` está no `.gitignore` e não deve ser enviado ao GitHub.

---

### ▶️ 5. Executar o Servidor

```bash
python run.py
```

Acesse no navegador:

```
http://localhost:5000
```

---

## 💡 Como Usar o Sistema

### 1️⃣ Upload do Arquivo

Selecione um arquivo `.csv` ou `.xlsx`.

### 2️⃣ Escrever a Instrução

Digite exatamente o que deseja que a IA investigue.

**Exemplo:**

> "Leia as avaliações desta planilha e identifique qual é a principal reclamação sobre a entrega"

### 3️⃣ Gerar Relatório

Clique em **Gerar Relatório Analítico**.

### 4️⃣ Visualizar Dashboard

O sistema exibirá um relatório estruturado contendo:

- 📌 Resumo Executivo  
- 📊 Principais Descobertas  
- 🎯 Resposta Direta ao Pedido  
- 🚀 Recomendações Estratégicas  

---

## 🎓 Objetivo Acadêmico

Este projeto demonstra a aplicação prática de:

- Engenharia de Prompt  
- Integração de APIs de IA Generativa  
- Manipulação de Dados com Pandas  
- Arquitetura MVC  
- Segurança de Aplicações  

---

## 📌 Licença

Projeto acadêmico desenvolvido para fins educacionais.
