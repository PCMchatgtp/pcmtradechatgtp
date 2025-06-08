import requests
from datetime import datetime
import pytz
from config import TWELVE_DATA_API_KEY

def recuperer_donnees(symbole):
    symbol_mapping = {
        "XAU/USD": "XAU/USD",
        "BTC/USD": "BTC/USD",
        "QQQ": "QQQ"
    }

    if symbole not in symbol_mapping:
        raise ValueError(f"❌ Symbole non pris en charge : {symbole}")

    url = f"https://api.twelvedata.com/time_series?symbol={symbol_mapping[symbole]}&interval=5min&apikey={TWELVE_DATA_API_KEY}&outputsize=50&dp=4"
    response = requests.get(url)
    data = response.json()

    if "values" not in data:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")

    valeurs = data["values"]

    donnees = []
    for valeur in valeurs:
        donnees.append({
            "datetime": valeur["datetime"],
            "open": float(valeur["open"]),
            "high": float(valeur["high"]),
            "low": float(valeur["low"]),
            "close": float(valeur["close"]),
            "volume": float(valeur["volume"])
        })

    heure_analyse = datetime.now(pytz.timezone("Europe/Paris")).strftime("%H:%M")
    indicateurs = {
        "derniere_close": donnees[0]["close"],
        "volume": donnees[0]["volume"]
    }

    return donnees, heure_analyse, indicateurs