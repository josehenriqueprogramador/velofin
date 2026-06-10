import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

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
    ticker: str = Query("PETR4"), 
    ano: int = Query(2024)
):
    # Limpa o ticker para o formato que a Brapi aceita
    clean_ticker = ticker.split('.')[0].upper()
    url = f"https://brapi.dev/api/quote/{clean_ticker}?token={BRAPI_TOKEN}&range=1y&interval=1d"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if "results" not in data or not data["results"]:
            raise HTTPException(status_code=404, detail="Ativo não encontrado")
        
        asset_data = data["results"][0]
        history = asset_data.get("historicalDataPrice", [])
        
        processed = []
        for item in history:
            # A API retorna o campo 'date' como um timestamp inteiro
            ts = item.get("date")
            if ts:
                dt_object = datetime.fromtimestamp(ts)
                
                # Filtra pelo ano solicitado
                if dt_object.year == ano:
                    processed.append({
                        "date": dt_object.strftime("%Y-%m-%d"),
                        "close": item.get("close"),
                        "volume": item.get("volume")
                    })

        return {
            "ticker": clean_ticker,
            "currentPrice": asset_data.get("regularMarketPrice"),
            "history": processed
        }
        
    except Exception as e:
        logger.error(f"Erro no processamento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
