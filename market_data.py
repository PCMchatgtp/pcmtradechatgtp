import requests
import os

from datetime import datetime, timedelta

ALPHAV_API_KEY = os.getenv("ALPHAV_API_KEY")

def recuperer_donnees(actif):
    symbol_map = {
        "NASDAQ": "QQQ",          # ETF Nasdaq
        "DAX": "DAX",             # Indice via Yahoo Finance
        "XAUUSD": "XAU/USD"       # Métal précieux
    }

    function_map = {
        "QQQ": "TIME_SERIES_INTRADAY",
        "DAX": "TIME_SERIES_INTRADAY",
        "XAU/USD": "FX_INTRADAY"
    }

    symbol = symbol_map.get(actif)
    if not symbol:
        raise ValueError(f"❌ Actif inconnu : {actif}")

    function = function_map[symbol]

    url = f"https://www.alphavantage.co/query"
    params = {
        "function": function,
        "symbol": symbol if function != "FX_INTRADAY" else "XAU/USD",
        "from_symbol": "XAU",
        "to_symbol": "USD",
        "interval": "5min",
        "apikey": ALPHAV_API_KEY,
        "outputsize": "compact"
    }

    response = requests.get(url, params=params)
    data = response.json()

    try:
        # Récupération des données selon le type
        if "Time Series (5min)" in data:
            values = data["Time Series (5min)"]
        elif "Time Series FX (5min)" in data:
            values = data["Time Series FX (5min)"]
        else:
            raise ValueError(f"❌ Données manquantes pour {actif} : {data}")

        close_prices = [float(v["4. close"]) for k, v in sorted(values.items())]
        return {"c": close_prices}

    except Exception as e:
        raise ValueError(f"❌ Erreur parsing Alpha Vantage : {e}")
