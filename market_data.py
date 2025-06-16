import requests
import datetime
import pytz
import time
from config import OPENAI_API_KEY

# 🧠 Cache local des données par symbole
_cache = {}

def recuperer_donnees(symbole, api_key):
    now = time.time()

    # Vérifie si les données en cache sont récentes (< 5 min)
    if symbole in _cache and now - _cache[symbole]["timestamp"] < 300:
        return _cache[symbole]["heure"], _cache[symbole]["indicateurs"]

    # 📊 Récupération des prix
    url_price = "https://api.twelvedata.com/time_series"
    params_price = {
        "symbol": symbole,
        "interval": "5min",
        "outputsize": 1,
        "apikey": api_key
    }

    # 📈 RSI
    url_rsi = "https://api.twelvedata.com/rsi"
    params_rsi = {
        "symbol": symbole,
        "interval": "5min",
        "time_period": 14,
        "apikey": api_key
    }

    # 📉 Moyennes mobiles
    url_ma = "https://api.twelvedata.com/ma"
    params_ma50 = {
        "symbol": symbole,
        "interval": "5min",
        "time_period": 50,
        "apikey": api_key
    }
    params_ma200 = {
        "symbol": symbole,
        "interval": "5min",
        "time_period": 200,
        "apikey": api_key
    }

    try:
        prix = requests.get(url_price, params=params_price).json()
        rsi = requests.get(url_rsi, params=params_rsi).json()
        ma50 = requests.get(url_ma, params=params_ma50).json()
        ma200 = requests.get(url_ma, params=params_ma200).json()

        if "values" not in prix or not prix["values"]:
            raise ValueError(f"❌ Erreur données prix : {prix}")
        candle = prix["values"][0]

        open_price = float(candle["open"])
        high_price = float(candle["high"])
        low_price = float(candle["low"])
        close_price = float(candle["close"])
        volume = candle.get("volume", "N/A")
        average_price = (high_price + low_price + close_price) / 3

        heure = datetime.datetime.now(pytz.timezone("Europe/Paris")).strftime("%Y-%m-%d %H:%M:%S")

        # RSI sécurisé
        rsi_value = "N/A"
        if "values" in rsi and isinstance(rsi["values"], list) and len(rsi["values"]) > 0:
            rsi_value = rsi["values"][0].get("rsi", "N/A")

        # Moyennes mobiles sécurisées
        ma_50 = None
        if "values" in ma50 and ma50["values"]:
            try:
                ma_50 = float(ma50["values"][0].get("ma"))
            except:
                pass

        ma_200 = None
        if "values" in ma200 and ma200["values"]:
            try:
                ma_200 = float(ma200["values"][0].get("ma"))
            except:
                pass

        tendance = "indéterminée"
        if ma_50 is not None and ma_200 is not None:
            if ma_50 > ma_200:
                tendance = "haussière"
            elif ma_50 < ma_200:
                tendance = "baissière"

        indicateurs = (
            f"Prix ouverture : {open_price}\n"
            f"Prix haut : {high_price}\n"
            f"Prix bas : {low_price}\n"
            f"Prix clôture : {close_price}\n"
            f"Volume : {volume}\n"
            f"Prix moyen : {average_price:.2f}\n"
            f"Range (H-L) : {high_price - low_price:.2f}\n"
            f"Taille corps : {abs(close_price - open_price):.2f}\n"
            f"RSI (14) : {rsi_value}\n"
            f"Tendance : {tendance}\n"
            f"Variation % : {((close_price - open_price) / open_price * 100):.2f}%"
        )

        # Sauvegarde en cache
        _cache[symbole] = {
            "timestamp": now,
            "heure": heure,
            "indicateurs": indicateurs
        }

        return heure, indicateurs

    except Exception as e:
        raise ValueError(f"❌ Erreur récupération {symbole} : {e}")
