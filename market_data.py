
import requests
from datetime import datetime

from config import TWELVE_DATA_API_KEY

def recuperer_donnees(symbole):
    base_url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbole,
        "interval": "5min",
        "outputsize": 1,
        "apikey": TWELVE_DATA_API_KEY
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if "values" not in data:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")

    dernier = data["values"][0]
    prix = float(dernier["close"])
    volume = float(dernier.get("volume", 0.0))
    heure = datetime.now().strftime("%H:%M")

    # Simuler d'autres indicateurs (à affiner selon accès réel)
    rsi = 50.0  # valeur neutre fictive
    ema = prix
    macd = 0.0

    # Déterminer tendance simple
    tendance = "hausse" if float(dernier["close"]) > float(dernier["open"]) else "baisse"

    return {
        "prix": prix,
        "volume": volume,
        "heure": heure,
        "rsi": rsi,
        "ema": ema,
        "macd": macd,
        "tendance": tendance
    }
