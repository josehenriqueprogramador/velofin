import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configuração de logs para ver o erro no painel do Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BRAPI_TOKEN = "demo"

@app.get("/api/v1/analytics")
async def get_market_data(
    ticker: str = Query("PETR4", min_length=3, max_length=10),
    ano: int = Query(2024, ge=2020)
):
    clean_ticker = ticker.split('.')[0].upper()
    url = f"https://brapi.dev/api/quote/{clean_ticker}?token={BRAPI_TOKEN}&range=1y&interval=1d"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # Loga a resposta da API para podermos ver no painel do Render
        logger.info(f"Resposta Brapi para {clean_ticker}: {data}")

        if response.status_code != 200 or "results" not in data:
            raise HTTPException(status_code=404, detail="Ativo não encontrado ou API indisponível.")
        
        asset_data = data["results"][0]
        history = asset_data.get("historicalDataPrice", [])
        
        # Processamento seguro dos dados
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
        logger.error(f"Erro no processamento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
