import requests
from config import FINNHUB_API_KEY

symbol_map = {
    "DAX": "^GDAXI",
    "NASDAQ": "^IXIC",
    "GOLD": "XAUUSD"
}

def recuperer_donnees(actif):
    symbole = symbol_map.get(actif.upper(), None)
    if not symbole:
        return "Actif non reconnu"

    url = f"https://finnhub.io/api/v1/crypto/candle?symbol=BINANCE:BTCUSDT&resolution=5&count=100&token={FINNHUB_API_KEY}"
    r = requests.get(url)
    data = r.json()
    return f"Prix actuel : {data.get('c')}, Haut : {data.get('h')}, Bas : {data.get('l')}, Ouverture : {data.get('o')}"
