# 📊 Analisador Inteligente de Dados com IA (Python + Gemini)

<p align="center">
  <b>Trabalho de Conclusão de Curso (TCC)</b><br>
  Bacharelado em Sistemas de Informação – 2026<br>
  <b>Autor:</b> José Carlos Cândido Ferreira
</p>

---

## 🧠 Stack Tecnológica

<div align="center">

<a href="https://www.python.org/doc/essays/blurb/" target="_blank">
  <img src="https://img.shields.io/badge/Python-Programação-3776AB?style=for-the-badge&logo=python&logoColor=white">
</a>

<a href="https://flask.palletsprojects.com/en/latest/quickstart/" target="_blank">
  <img src="https://img.shields.io/badge/Flask-Framework%20Web-000000?style=for-the-badge&logo=flask&logoColor=white">
</a>

<a href="https://pandas.pydata.org/docs/getting_started/overview.html" target="_blank">
  <img src="https://img.shields.io/badge/Pandas-Processamento%20de%20Dados-150458?style=for-the-badge&logo=pandas">
</a>

<a href="https://ai.google.dev/docs/gemini_api_overview" target="_blank">
  <img src="https://img.shields.io/badge/Google%20Gemini-IA%20Generativa-8E75B2?style=for-the-badge">
</a>

<a href="https://developer.mozilla.org/pt-BR/docs/Web/HTML" target="_blank">
  <img src="https://img.shields.io/badge/HTML5-Estrutura%20Web-E34F26?style=for-the-badge&logo=html5&logoColor=white">
</a>

<a href="https://tailwindcss.com/docs" target="_blank">
  <img src="https://img.shields.io/badge/Tailwind%20CSS-Estilização-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white">
</a>

</div>

---

## 🎥 Demonstração da Interface

<p align="center">
  <img src="interface.png" width="850px" style="border-radius: 12px;">
</p>

---

# 💻 Sobre o Projeto

O **Analisador Inteligente de Dados** é uma aplicação web desenvolvida com **Python + Flask**, criada para automatizar a interpretação de grandes volumes de dados textuais não estruturados.

O sistema resolve um problema real:

> 🔎 Transformar feedbacks, avaliações e comentários qualitativos em relatórios estratégicos estruturados automaticamente.

A aplicação integra:

- 📊 **Pandas** → Leitura e pré-processamento de `.csv` e `.xlsx`
- 🤖 **Google Gemini API** → Análise com IA Generativa
- 🌐 **HTML + CSS (Tailwind)** → Interface web responsiva

O resultado é um **relatório analítico estruturado em tempo real**, pronto para tomada de decisão.

---

# 🛡️ Diferencial Técnico — Mitigação de Alucinações da IA

Este projeto foi arquitetado com foco em **confiabilidade e precisão analítica**, implementando controles técnicos robustos:

### 🔐 1. Grounding (Ancoragem)

O prompt contém instruções explícitas proibindo a invenção de dados.

### 📄 2. Contexto Integral

Uso de:

```python
df.to_csv(index=False)
```

Garantindo que **100% dos dados** sejam enviados para análise.

### 🎛️ 3. Configuração Determinística

Chamada da API com:

```python
temperature=0.1
```

Reduzindo criatividade e aumentando previsibilidade e consistência.

---

# 🏗️ Arquitetura do Projeto

Organização baseada em **MVC Adaptado**, separando responsabilidades:

```text
tcc-jose/
│
├── run.py
├── .env
├── requirements.txt
├── README.md
├── interface.png
│
└── app/
    ├── routes.py
    ├── services/
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

📌 Separação clara entre:
- Rotas
- Regras de negócio
- Construção de prompt
- Interface

---

# 🚀 Como Executar o Projeto

## 1️⃣ Clonar o Repositório

```bash
git clone https://github.com/josecarlosjccf/tcc-jose.git
cd tcc-jose
```

---

## 2️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Configurar Variáveis de Ambiente

Crie um `.env`:

```env
GEMINI_API_KEY="SUA_CHAVE_AQUI"
GEMINI_VERSION="2.5"
```

⚠️ Nunca envie o `.env` para o GitHub.

---

## 4️⃣ Executar

```bash
python run.py
```

Acesse:

```
http://localhost:5000
```

---

# 🧩 Fluxo de Uso do Sistema

### 📤 1. Upload

Envie um arquivo `.csv` ou `.xlsx`.

### ✍️ 2. Instrução

Descreva exatamente o que deseja investigar.

Exemplo:

> "Identifique a principal reclamação sobre atraso na entrega."

### 📊 3. Relatório Gerado

O sistema entrega:

- 📌 Resumo Executivo  
- 📊 Principais Insights  
- 🎯 Resposta Direta  
- 🚀 Recomendações Estratégicas  

---

# 🎓 Contribuição Acadêmica

Este projeto demonstra domínio em:

- Engenharia de Prompt
- Integração de APIs REST
- Manipulação de Dados com Pandas
- Arquitetura MVC
- Segurança Aplicacional
- IA Generativa aplicada a negócios

---

# 📈 Possíveis Evoluções Futuras

- Dashboard com gráficos interativos
- Armazenamento de histórico de análises
- Autenticação de usuários
- Deploy em nuvem (AWS ou GCP)
- Containerização com Docker

---

# 📜 Licença

Projeto acadêmico desenvolvido para fins educacionais.