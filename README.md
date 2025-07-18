# 📚 Book Public API

API pública para consulta de livros, criada como infraestrutura inicial para futuros sistemas de recomendação com machine learning.

## 🚀 Visão Geral

Este projeto visa disponibilizar uma API REST pública contendo dados estruturados de livros. A API foi construída com foco em escalabilidade, modularidade e futura integração com sistemas de recomendação.

## 🧱 Arquitetura

A arquitetura segue os princípios de separação de responsabilidades, com os seguintes módulos:

- **api/**: estrutura da FastAPI com rotas e dependências.
- **scripts/**: scripts de ETL (extração, transformação e carga) dos dados.
- **data/**: armazenamento local de dados brutos e transformados.
- **tests/**: testes automatizados para validar comportamento da API.

## 🛠️ Instalação

```bash
git clone https://github.com/seu-usuario/techChallenge.git
cd techChallenge
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
