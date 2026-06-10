import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(
    title="VeloFin API",
    description="API robusta de dados financeiros via Brapi",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Token 'demo' funciona para testes, para produção considere obter um em brapi.dev
BRAPI_TOKEN = "demo"

@app.get("/api/v1/analytics")
async def get_market_data(
    ticker: str = Query("PETR4", min_length=3, max_length=10),
    ano: int = Query(2024, ge=2020)
):
    # Limpa o ticker (remove .SA se o usuário enviar, pois a Brapi usa o código puro)
    clean_ticker = ticker.split('.')[0].upper()
    
    # URL da API Brapi
    url = f"https://brapi.dev/api/quote/{clean_ticker}?token={BRAPI_TOKEN}&range=1y&interval=1d"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Erro ao conectar com provedor de dados.")
        
        data = response.json()
        
        if "results" not in data or not data["results"]:
            raise HTTPException(status_code=404, detail="Ativo não encontrado.")
        
        # Extrai os dados
        asset_data = data["results"][0]
        history = asset_data.get("historicalDataPrice", [])
        
        # Filtra pelo ano solicitado se necessário
        processed = [
            {
                "date": item.get("date"),
                "close": item.get("close"),
                "volume": item.get("volume")
            }
            for item in history 
            if item.get("date", "").startswith(str(ano))
        ]

        return {
            "ticker": clean_ticker,
            "currentPrice": asset_data.get("regularMarketPrice"),
            "history": processed
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
