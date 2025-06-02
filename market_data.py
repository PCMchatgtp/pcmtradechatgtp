import requests
import time
from config import TWELVE_API_KEY

def recuperer_donnees(actif):
    symbol_map = {
    "DAX": "GDAXI",          # Indice DAX (Allemagne)
    "NASDAQ": "IXIC",        # Indice Nasdaq Composite
    "XAUUSD": "XAU/USD"      # Or contre dollar (ça fonctionne déjà)
}

    symbol = symbol_map.get(actif)
    if not symbol:
        raise ValueError(f"❌ Actif non reconnu : {actif}")

    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": "5min",
        "apikey": TWELVE_API_KEY,
        "outputsize": 100
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "values" not in data:
        raise ValueError(f"❌ Données invalides de TwelveData pour {actif} : {data}")

    # Extraire uniquement les prix de clôture dans l’ordre chronologique
    close_prices = [float(item["close"]) for item in reversed(data["values"])]

    return {"c": close_prices}
