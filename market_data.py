import requests
from config import FINNHUB_API_KEY

def recuperer_donnees(actif):
    symbol_map = {
        "DAX": "INDEX:DEU40",
        "NASDAQ": "US:NDX",
        "XAUUSD": "OANDA:XAU_USD"
    }

    symbol = symbol_map.get(actif)
    if not symbol:
        raise ValueError(f"Symbole inconnu pour l’actif {actif}")

    url = f"https://finnhub.io/api/v1/crypto/candle?symbol={symbol}&resolution=5&count=100&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    data = response.json()  # ✅ Important

    # Exemple d’accès sécurisé
    if data.get("s") != "ok":
        raise ValueError(f"API Finnhub n’a pas retourné de données valides pour {actif}")

    return data  # ou data['c'] si tu veux uniquement les prix de clôture
