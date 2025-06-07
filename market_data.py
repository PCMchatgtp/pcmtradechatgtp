import requests
from config import TWELVE_DATA_API_KEY

def recuperer_donnees(symbole):
    url = f"https://api.twelvedata.com/time_series?symbol={symbole}&interval=5min&apikey={TWELVE_DATA_API_KEY}&outputsize=5"
    reponse = requests.get(url)
    data = reponse.json()
    if "values" not in data:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")
    return data["values"]