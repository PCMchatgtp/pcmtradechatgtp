
import requests
from datetime import datetime

def recuperer_donnees(symbole, api_key):
    url = f"https://api.twelvedata.com/time_series?symbol={symbole}&interval=5min&outputsize=1&apikey={api_key}"
    reponse = requests.get(url)
    data = reponse.json()

    if 'values' not in data:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")

    derniere = data["values"][0]
    heure = derniere["datetime"]

    indicateurs = {
        "open": derniere["open"],
        "high": derniere["high"],
        "low": derniere["low"],
        "close": derniere["close"],
        "volume": derniere.get("volume", "Non disponible")
    }

    return {"heure": heure, "indicateurs": indicateurs}
