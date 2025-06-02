import requests
from config import RAPIDAPI_KEY

def recuperer_donnees(actif):
    symbol_map = {
        "DAX": "^GDAXI",
        "NASDAQ": "^NDX",
        "XAUUSD": "GC=F"
    }

    symbol = symbol_map.get(actif)
    if not symbol:
        raise ValueError(f"❌ Actif inconnu : {actif}")

    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    params = {"symbol": symbol, "region": "US"}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise ValueError(f"❌ API Yahoo Finance a échoué pour {actif} : {response.text}")

    data = response.json()

    try:
        prix = data["price"]["regularMarketPrice"]["raw"]
        return {"c": [prix] * 100}
    except Exception:
        raise ValueError(f"❌ Impossible d’extraire le prix pour {actif}")
