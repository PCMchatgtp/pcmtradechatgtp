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

        # Nettoyage
        open_price = float(candle["open"])
        high_price = float(candle["high"])
        low_price = float(candle["low"])
        close_price = float(candle["close"])
        volume = candle.get("volume", "N/A")

        heure = datetime.datetime.now(pytz.timezone("Europe/Paris")).strftime("%Y-%m-%d %H:%M:%S")

        # Indicateurs enrichis
        indicateurs = {
            "open": str(open_price),
            "high": str(high_price),
            "low": str(low_price),
            "close": str(close_price),
            "volume": volume,
            "datetime": candle.get("datetime", "N/A"),
            "average_price": str((high_price + low_price + close_price) / 3),
            "range": str(high_price - low_price),
            "body_size": str(abs(close_price - open_price)),
            "upper_wick": str(high_price - max(open_price, close_price)),
            "lower_wick": str(min(open_price, close_price) - low_price),
            "bullish": str(close_price > open_price),
            "percentage_change": str(((close_price - open_price) / open_price) * 100)
        }

        return heure, indicateurs

    except Exception as e:
        raise ValueError(f"❌ Erreur lors de la récupération de {symbole} : {e}")
