📊 API Health & Metrics

Uma aplicação desenvolvida com FastAPI para monitorar o status da API, registrar métricas de uso e exibir um painel de visualização com Streamlit.

Ela também expõe uma rota para busca de livros fictícios e grava logs estruturados e métricas de chamadas HTTP em um banco SQLite.

🔧 Tecnologias utilizadas

✅ Python 3.8+

✅ FastAPI

✅ Uvicorn

✅ SQLite

✅ Streamlit

✅ Plotly (gráficos)

✅ Logging JSON estruturado

📁 Estrutura do Projeto

<img width="775" height="445" alt="figura 1" src="https://github.com/user-attachments/assets/3bfe3c66-cbd5-4bab-8751-b0bd5e47c8f1" />

🚀 Como instalar e rodar

1. Clone o repositório
   
git clone git@github.com:CindyKanashiro/techChallenge.git

cd techChallenge

git checkout API-Health-Metrics

4. Crie e ative um ambiente virtual

python3 -m venv venv

source venv/bin/activate     # Linux/macOS

venv\Scripts\activate        # Windows

5. Instale as dependências

pip install -r requirements.txt

▶️ Rodando a API

Execute a API com:

uvicorn api.main:app --reload

Acesse:

📘 Swagger: http://localhost:8000/docs

📘 Redoc: http://localhost:8000/redoc

🔍 Endpoints principais

Método	Caminho	Descrição

GET	/api/v1/health	Verifica se a API está funcionando

GET	/api/v1/metrics	Retorna métricas agregadas da API

GET	/api/v1/metrics/detailed	Mostra todas as requisições registradas

GET	/api/v1/books/search	Busca por livros por título, autor e categoria

📌 Exemplos de uso:

GET /api/v1/books/search?title=python&category=tecnologia

GET /api/v1/health

📈 Visualizar métricas no dashboard

Execute:

streamlit run dashboard.py

Acesse: http://localhost:8501

Exibe:

Total de requisições por rota

Tempo médio de resposta

Tabela com histórico detalhado

Gráficos interativos com Plotly

📦 requirements.txt
fastapi

uvicorn

streamlit

requests

plotly

✅ Logs

Todos os acessos são:

Registrados como JSON em api.log

Armazenados no banco metrics.db com:

Timestamp

Método

Caminho

Status HTTP

Duração da requisição (ms)

⚠️ Observações

O banco metrics.db é criado automaticamente na primeira execução.

Nenhum dado é persistido fora do SQLite por padrão.

A API aceita filtros combinados (AND) para title, author, category.

📜 Licença
MIT License © 2025 — Claudio Lavezzo Junior

