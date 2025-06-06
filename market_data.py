import requests
from config import TWELVE_DATA_API_KEY

def recuperer_donnees(symbole):
    try:
        url = f"https://api.twelvedata.com/time_series?symbol={symbole}&interval=5min&outputsize=5&apikey={TWELVE_DATA_API_KEY}"
        response = requests.get(url)
        data = response.json()
        if "values" not in data:
            raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")
        latest = data["values"][0]
        return {
            "price": float(latest["close"]),
            "volume": float(latest["volume"]),
            "high": float(latest["high"]),
            "low": float(latest["low"]),
            "timestamp": latest["datetime"]
        }
    except Exception as e:
        raise RuntimeError(f"❌ Erreur lors de la récupération de {symbole} : {e}")