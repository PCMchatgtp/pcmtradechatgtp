import requests
import datetime
import pytz
from config import OPENAI_API_KEY

def recuperer_donnees(symbole, api_key):
    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbole,
        "interval": "5min",
        "outputsize": 1,
        "apikey": api_key
    }
    try:
        reponse = requests.get(url, params=params)
        data = reponse.json()
        if "values" not in data:
            raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")
        candle = data["values"][0]
        heure = datetime.datetime.now(pytz.timezone("Europe/Paris")).strftime("%Y-%m-%d %H:%M:%S")
        indicateurs = {
            "open": candle["open"],
            "high": candle["high"],
            "low": candle["low"],
            "close": candle["close"],
            "volume": candle.get("volume", "N/A")
        }
        return heure, indicateurs
    except Exception as e:
        raise ValueError(f"❌ Erreur lors de la récupération de {symbole} : {e}")