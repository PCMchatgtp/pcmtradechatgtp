import requests
from config import SYMBOLS, TWELVE_API_KEY

def recuperer_donnees(actif):
    symbol = SYMBOLS.get(actif)
    if not symbol:
        raise ValueError(f"Symbole introuvable pour {actif}")

    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "price" not in data:
        raise ValueError(f"Données invalides de TwelveData pour {actif} : {data}")

    return {
        "actif": actif,
        "prix": float(data["price"])
    }