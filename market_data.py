import requests
import os
from datetime import datetime

API_KEY = os.getenv("TWELVE_DATA_API_KEY")
BASE_URL = "https://api.twelvedata.com/price"

def recuperer_donnees(actif, symbole):
    try:
        params = {
            "symbol": symbole,
            "apikey": API_KEY
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if "price" not in data:
            raise ValueError(f"❌ Données invalides de TwelveData pour {actif} : {data}")

        return {
            "actif": actif,
            "prix": float(data["price"]),
            "heure": datetime.utcnow(),
            "tendance": "hausse" if float(data["price"]) % 2 == 0 else "baisse"
        }
    except Exception as e:
        raise ValueError(f"❌ Erreur lors de la récupération de {actif} : {e}")
