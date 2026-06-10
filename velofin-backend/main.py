import os
import asyncio
import logging
from datetime import datetime
import pandas as pd
import yfinance as yf
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests_cache

# Configuração de cache para evitar sobrecarga no Yahoo
session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_data(ticker: str, ano: int):
    try:
        # Usando a sessão configurada com User-Agent
        ticker_obj = yf.Ticker(ticker, session=session)
        df = ticker_obj.history(
            start=f"{ano}-01-01",
            end=datetime.now().strftime("%Y-%m-%d")
        )
        
        if df.empty:
            return pd.DataFrame()
            
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
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        raw_close = df["Close"].iloc[-1]
        preco_atual = round(float(raw_close), 2)

        df_recent = df.reset_index()
        for _, row in df_recent.iterrows():
            registos_limpos.append({
                "date": row['Date'].strftime("%d/%m/%Y"),
                "close": round(float(row["Close"]), 2),
                "volume": int(row["Volume"])
            })
    except Exception as e:
        logger.error(f"Erro no processamento: {e}")
        return [], 0.0
    return registos_limpos, preco_atual

@app.get("/api/v1/analytics")
async def get_market_data(ticker: str = "PETR4.SA", ano: int = 2024):
    df = await asyncio.to_thread(fetch_data, ticker, ano)
    if df.empty:
        raise HTTPException(status_code=404, detail=f"Dados vazios para {ticker}. Tente outro ticker ou verifique a conexão.")
    registros, preco_atual = process_data(df)
    return {"ticker": ticker.upper(), "currentPrice": preco_atual, "history": registros}
