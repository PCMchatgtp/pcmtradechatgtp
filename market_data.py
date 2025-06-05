import requests
import os
from datetime import datetime
import pytz

API_KEY = os.getenv("TWELVE_DATA_API_KEY")

SYMBOLS_MAPPING = {
    "XAUUSD": "XAU/USD",
    "BTCUSD": "BTC/USD",
    "NASDAQ": "NDX/USD"  # Assure-toi que ce symbole est bien reconnu par Twelve Data
}

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

def analyser_tendance(donnees):
    # Simpliste : on compare les deux derniers cours
    try:
        prix_actuel = float(donnees["prix"])
        return "hausse" if prix_actuel > 0 else "baisse"  # à personnaliser selon ta logique réelle
    except:
        return "indéterminée"

def heure_actuelle():
    paris_tz = pytz.timezone("Europe/Paris")
    maintenant = datetime.now(paris_tz)
    return maintenant.strftime("%H:%M")
