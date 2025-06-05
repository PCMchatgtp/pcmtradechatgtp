import requests

SYMBOLS_MAPPING = {
    "XAUUSD": "XAU/USD",
    "BTCUSD": "BTC/USD",
    "NASDAQ": "QQQ"
}

from config import TWELVE_DATA_API_KEY

def recuperer_donnees(actif):
    symbole = SYMBOLS_MAPPING.get(actif)
    if not symbole:
        raise ValueError(f"❌ Symbole introuvable pour {actif}")

    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbole,
        "interval": "5min",
        "apikey": API_KEY,
        "outputsize": 2
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "status" in data and data["status"] == "error":
        raise ValueError(f"❌ Données invalides de TwelveData pour {actif} : {data}")

    try:
        latest = data["values"][0]
        return {
            "prix": float(latest["close"]),
            "timestamp": latest["datetime"]
        }
    except (KeyError, IndexError, ValueError) as e:
        raise ValueError(f"❌ Erreur lors du parsing des données {actif} : {e}")
