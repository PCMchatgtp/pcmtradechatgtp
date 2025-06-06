
import requests
from datetime import datetime
import pytz

def recuperer_donnees(symbole, twelve_data_api_key):
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbole,
        "interval": "5min",
        "outputsize": 30,
        "apikey": twelve_data_api_key
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "values" not in data:
            raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")

        return data["values"]

    except Exception as e:
        raise ValueError(f"❌ Erreur lors de la récupération de {symbole} : {e}")
