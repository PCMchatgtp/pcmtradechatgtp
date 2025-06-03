import requests
from config import TWELVE_DATA_API_KEY, SYMBOLS

def recuperer_donnees(actif):
    symbol = SYMBOLS.get(actif)
    if not symbol:
        raise ValueError(f"❌ Symbole introuvable pour {actif}")

    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_DATA_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "price" not in data:
        raise ValueError(f"❌ Données invalides de TwelveData pour {actif} : {data}")

    prix = float(data["price"])
    return {
        "actif": actif,
        "prix": prix
    }
