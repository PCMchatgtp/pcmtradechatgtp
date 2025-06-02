import requests
from config import FMP_API_KEY

def recuperer_donnees(actif):
    symbol_map = {
        "DAX": "^GDAXI",
        "NASDAQ": "^NDX",
        "XAUUSD": "XAUUSD"
    }

    symbol = symbol_map.get(actif)
    if not symbol:
        raise ValueError(f"❌ Symbole inconnu pour l’actif {actif}")

    url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={FMP_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if not isinstance(data, list) or len(data) == 0 or "price" not in data[0]:
        raise ValueError(f"❌ FMP n’a pas retourné de prix valide pour {actif}")

    prix = data[0]["price"]
    return {"c": [prix] * 100}  # on simule une série de données

