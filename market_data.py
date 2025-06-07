
import requests

def recuperer_donnees(symbole, api_key):
    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbole,
        "interval": "5min",
        "outputsize": 30,
        "apikey": api_key
    }

    reponse = requests.get(url, params=params)
    donnees = reponse.json()

    if "values" not in donnees:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {donnees}")

    return donnees["values"]
