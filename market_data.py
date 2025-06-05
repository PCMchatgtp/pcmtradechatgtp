import requests

def recuperer_donnees(symbole):
    from config import os

    api_key = os.getenv("TWELVE_DATA_API_KEY")
    url = f"https://api.twelvedata.com/time_series?symbol={symbole}&interval=5min&apikey={api_key}&outputsize=5"
    r = requests.get(url)
    data = r.json()

    if "values" not in data:
        raise ValueError(f"❌ Données invalides de TwelveData pour {symbole} : {data}")

    return data["values"]
