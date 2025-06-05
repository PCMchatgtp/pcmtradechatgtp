
import requests
from datetime import datetime
import pytz
from config import TWELVE_API_KEY, SYMBOLS

def recuperer_donnees(actif):
    base_url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": SYMBOLS[actif]["symbol"],
        "interval": "5min",
        "outputsize": 1,
        "apikey": TWELVE_API_KEY
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if "values" not in data:
            raise ValueError(f"❌ Données invalides de TwelveData pour {actif} : {data}")
        prix = float(data["values"][0]["close"])
        return {"actif": actif, "prix": prix}
    except Exception as e:
        raise ValueError(f"❌ Erreur lors de la récupération de {actif} : {e}")

def heure_actuelle():
    tz = pytz.timezone("Europe/Paris")
    return datetime.now(tz).hour

def actif_dans_horaire(actif):
    heure = heure_actuelle()
    debut = SYMBOLS[actif]["heure_debut"]
    fin = SYMBOLS[actif]["heure_fin"]
    return debut <= heure <= fin
