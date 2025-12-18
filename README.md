# 🤖 Juma Agent AI

> Assistente de Inteligência Artificial para análise de dados corporativos, conectado diretamente ao Data Warehouse (BigQuery). Utiliza **Google Gemini**, **Python** e **Scikit-Learn** para gerar queries SQL, insights estratégicos e previsões de vendas (ML) em tempo real. [file:1]

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white) [file:1]
![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange?logo=google&logoColor=white) [file:1]
![BigQuery](https://img.shields.io/badge/Data-BigQuery-4285F4?logo=google-cloud&logoColor=white) [file:1]
![UV](https://img.shields.io/badge/Package-UV-purple?logo=python&logoColor=white) [file:1]

---

## 🎯 O que este projeto faz?

O **Juma Agent** é uma API inteligente que atua como um analista de dados sênior, recebendo perguntas em linguagem natural e orquestrando ferramentas técnicas para responder. [file:1]  
Ele suporta: [file:1]

1. **SQL Generativo:** Converte perguntas (por exemplo, “Qual o faturamento de ontem?”) em queries SQL complexas para o BigQuery. [file:1]  
2. **Machine Learning Forecast:** Utiliza modelos de Regressão Linear com ajuste de sazonalidade para projetar vendas futuras (12 meses). [file:1]  
3. **Visualização de Dados:** Gera gráficos dinâmicos e tabelas formatadas. [file:1]  
4. **Análise Comparativa (YoY):** Compara automaticamente o desempenho atual com o ano anterior. [file:1]

---

## 📂 Estrutura do projeto

O projeto segue o **App Pattern** para organização profissional. [file:1]

.
├── app/ # Código fonte da aplicação (pacote Python)
│ ├── main.py # API Flask e orquestração
│ ├── tools.py # Ferramentas (SQL e ML Forecast)
│ ├── config.py # Configurações e clientes GCP
│ ├── prompts.py # Prompts do sistema e schemas
│ └── utils.py # Utilitários auxiliares
├── scripts/ # Scripts de deploy e automação
├── Dockerfile # Configuração de container
├── pyproject.toml # Dependências (UV)
└── uv.lock # Lockfile (UV)

## 🚀 Como rodar localmente

Este projeto utiliza o **uv** para gerenciamento ultrarrápido de dependências. [file:1]

### 1. Pré-requisitos

- Python 3.10+ instalado. [file:1]  
- `uv` instalado. [file:1]  
- Credencial do Google Cloud (`service_account.json`). [file:1]

### 2. Instalação

Clone o repositório e sincronize o ambiente.

git clone https://github.com/Creattive-cc/juma-agent-IA.git
cd juma-agent-IA

### 3. Configuração de credenciais (importante)

Para acessar o BigQuery e a Vertex AI: [file:1]

- Baixe sua chave JSON de Conta de Serviço no Google Cloud. [file:1]  
- Renomeie o arquivo para `service_account.json`. [file:1]  
- Mova o arquivo para a raiz do projeto (ao lado do `pyproject.toml`). [file:1]  

🔒 Por segurança, `service_account.json` está no `.gitignore` para evitar vazamentos. [file:1]

### 4. Executando a aplicação

Como o código está organizado em um pacote (`app`), utilize a flag `-m` para rodar.
uv run -m app.main

O servidor iniciará em: http://127.0.0.1:8080.

### 5. Testando a API

Em um novo terminal, envie uma requisição:
curl -X POST http://127.0.0.1:8080/chat
-H "Content-Type: application/json"
-d '{"message": "Qual foi o faturamento total do ano passado?"}'

## 🐳 Como rodar com Docker

O `Dockerfile` está otimizado para usar o **uv** dentro do container, garantindo builds rápidos. [file:1]

### Construir a imagem
docker build -t juma-agent

### Rodar o container
> Nota: Se rodar localmente via Docker, certifique-se de montar o volume da chave ou copiá-la no build.

---

## ☁️ Deploy no Google Cloud Run

Para subir o projeto em produção, utilize os scripts automatizados na pasta `scripts/`

## 👨‍💻 Autor

Desenvolvido por **Felipe Malveira**. 