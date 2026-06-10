<div align="center">

# 📊 Velofin
### Análise Quantitativa e Inteligência Visual de Ativos

[![Status](https://img.shields.io/badge/status-ativo-success.svg)]()
[![Frontend](https://img.shields.io/badge/frontend-React-blue.svg)]()
[![Backend](https://img.shields.io/badge/backend-Python-green.svg)]()

*Transforme dados brutos de mercado em insights visuais de alta performance.*

</div>

---

## 📑 Sobre o Projeto
O **Velofin** é uma plataforma *full-stack* desenvolvida para fornecer análises financeiras ágeis. Combinando o poder de processamento do **Pandas** no backend com a interatividade do **Recharts** no frontend, o sistema permite que investidores visualizem o histórico de fechamento de ativos de forma clara e intuitiva.

## 🛠️ Tecnologias Principais
*   **Frontend**: React.js, SASS, Recharts.
*   **Backend**: Python, Pandas, YFinance (API de dados financeiros).
*   **Comunicação**: REST API.

---

## 🚀 Guia de Instalação (Passo a Passo)

Para rodar o projeto localmente, certifique-se de ter o **Node.js** e **Python** instalados.

### 1. Preparando o Backend
1. Entre na pasta do backend: `cd velofin-backend`
2. Instale as bibliotecas necessárias: `pip install -r requirements.txt`
3. Inicie o servidor: `python main.py`

### 2. Preparando o Frontend
1. Em um novo terminal, entre na pasta do frontend: `cd velofin-frontend`
2. Instale as dependências: `npm install`
3. Inicie a interface de desenvolvimento: `npm run dev`

---

## 📊 Como Utilizar
1. Acesse o endereço local gerado pelo terminal do frontend (ex: `http://localhost:5173`).
2. **Ticker**: Digite o código do ativo (Ex: `PETR4.SA` para Brasil, `AAPL` para EUA).
3. **Ano**: Selecione o ano inicial desejado.
4. Clique em **Analisar** para carregar os dados e o gráfico.

---

## 💡 Dicas de Ativos
O sistema aceita qualquer ativo listado no Yahoo Finance:
*   **Brasil**: `VALE3.SA`, `ITUB4.SA`, `WEGE3.SA`
*   **Internacional**: `MSFT`, `NVDA`, `TSLA`
*   **Cripto**: `BTC-USD`, `ETH-USD`

---
<div align="center">
  <sub>Desenvolvido com foco em performance e clareza.</sub>
</div>
