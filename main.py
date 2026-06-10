import os
import asyncio
import logging
from datetime import datetime
import pandas as pd
import yfinance as yf
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Inicialização do App
app = FastAPI(
    title="VeloFin API",
    description="Backend de alta performance para análise de ativos financeiros",
    version="1.0.0"
)

# 🔐 CONFIGURAÇÃO DE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_data(ticker: str, ano: int):
    try:
        # Configuração estável para o Render
        df = yf.download(
            ticker,
            start=f"{ano}-01-01",
            end=datetime.now().strftime("%Y-%m-%d"),
            progress=False,
            threads=False
        )
        
        if df.empty:
            return pd.DataFrame()
            
        # Limpeza de timezone para evitar erros no Pandas
        if hasattr(df.index, 'tz') and df.index.tz is not None:
            df.index = df.index.tz_localize(None)
            
        return df
    except Exception as e:
        logger.error(f"Erro no yfinance para {ticker}: {e}")
        return pd.DataFrame()

def process_data(df: pd.DataFrame):
    registos_limpos = []
    preco_atual = 0.0

    if df is None or df.empty:
        return registos_limpos, preco_atual

    try:
        # Corrige o MultiIndex se necessário
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Extrai o último preço de fechamento
        raw_close = df["Close"].iloc[-1]
        if hasattr(raw_close, "__len__") and not isinstance(raw_close, (str, bytes)):
            raw_close = raw_close[0]
        preco_atual = round(float(raw_close), 2)

        # Processa histórico
        df_recent = df.reset_index()
        date_col = "Date" if "Date" in df_recent.columns else df_recent.columns[0]

        for _, row in df_recent.iterrows():
            d_val = row[date_col]
            registos_limpos.append({
                "date": d_val.strftime("%d/%m/%Y") if hasattr(d_val, "strftime") else str(d_val),
                "close": round(float(row["Close"]), 2),
                "volume": int(row["Volume"])
            })
    except Exception as e:
        logger.error(f"Erro no processamento dos dados: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar dados.")

    return registos_limpos, preco_atual

@app.get("/api/v1/analytics")
async def get_market_data(
    ticker: str = Query("PETR4.SA", min_length=3, max_length=15),
    ano: int = Query(2024, ge=2000, le=datetime.now().year)
):
    df = await asyncio.to_thread(fetch_data, ticker, ano)

    if df.empty:
        raise HTTPException(status_code=404, detail=f"Nenhum dado encontrado para o ticker {ticker}.")

    registros, preco_atual = process_data(df)

    return {
        "ticker": ticker.upper(),
        "currentPrice": preco_atual,
        "history": registros
    }
