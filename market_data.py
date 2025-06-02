import requests
from config import FINNHUB_API_KEY, FMP_API_KEY

def recuperer_donnees(actif):
    if actif == "XAUUSD":
        # API FinancialModelingPrep pour l'or
        url = f"https://financialmodelingprep.com/api/v3/quote/XAUUSD?apikey={FMP_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if not data or "price" not in data[0]:
            raise ValueError("❌ FMP n’a pas retourné de prix valide pour l’or")

        prix = data[0]["price"]
        return {"c": [prix] * 100}  # On simule 100 prix identiques

    # Symboles Finnhub pour les autres actifs
    symbol_map = {
        "DAX": "INDEX:DEU40",
        "NASDAQ": "US:NDX"
    }

    symbol = symbol_map.get(actif)
    if not symbol:
        raise ValueError(f"❌ Symbole inconnu pour l’actif {actif}")

    url = f"https://finnhub.io/api/v1/index/candle?symbol={symbol}&resolution=5&count=100&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get("s") != "ok":
        raise ValueError(f"❌ API Finnhub n’a pas retourné de données valides pour {actif}")

    return data  # Contient 'c', 'o', 'h', 'l', 't', 's'
