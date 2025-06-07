
import requests

def recuperer_donnees_twelvedata(symbole, api_key):
    url = f"https://api.twelvedata.com/time_series?symbol={symbole}&interval=5min&outputsize=30&apikey={api_key}"
    response = requests.get(url)
    donnees = response.json()

    if "values" not in donnees:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {donnees}")

    return donnees["values"]
