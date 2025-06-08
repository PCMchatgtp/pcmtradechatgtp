import requests
import datetime

def recuperer_donnees(symbole, api_key):
    params = {
        "symbol": symbole,
        "interval": "5min",
        "outputsize": 5,
        "apikey": api_key
    }
    url = "https://api.twelvedata.com/time_series"
    response = requests.get(url, params=params)
    data = response.json()

    if "values" not in data:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")

    candles = data["values"]
    derniere = candles[0]
    heure = derniere["datetime"]
    tendance = "hausse" if float(derniere["close"]) > float(derniere["open"]) else "baisse"

    indicateurs = {
        "open": derniere.get("open"),
        "close": derniere.get("close"),
        "high": derniere.get("high"),
        "low": derniere.get("low"),
        "volume": derniere.get("volume", "N/A")
    }

    return tendance, heure, indicateurs