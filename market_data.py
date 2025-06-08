import requests
from config import OPENAI_API_KEY
from datetime import datetime
import pytz

def recuperer_donnees(symbole):
    base_url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbole,
        "interval": "5min",
        "outputsize": 1,
        "apikey": OPENAI_API_KEY
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "values" not in data:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")

    valeurs = data["values"][0]
    heure = datetime.now(pytz.timezone("Europe/Paris")).strftime("%H:%M:%S")

    indicateurs = {
        "open": float(valeurs["open"]),
        "high": float(valeurs["high"]),
        "low": float(valeurs["low"]),
        "close": float(valeurs["close"]),
        "volume": float(valeurs["volume"])
    }

    return valeurs, heure, indicateurs