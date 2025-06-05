import requests
import os

TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

def recuperer_donnees(symbole):
    url = f"https://api.twelvedata.com/time_series?symbol={symbole}&interval=5min&apikey={TWELVE_DATA_API_KEY}&outputsize=1"
    reponse = requests.get(url)
    data = reponse.json()

    if "values" not in data:
        raise ValueError(f"❌ Données invalides de TwelveData pour {symbole} : {data}")

    derniere = data["values"][0]
    prix = float(derniere["close"])
    return {"symbole": symbole, "prix": prix}