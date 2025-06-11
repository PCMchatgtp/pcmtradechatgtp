import requests
import datetime
import pytz
from config import OPENAI_API_KEY

def recuperer_donnees(symbole, api_key):
    # 📊 Récupération des prix
    url_price = f"https://api.twelvedata.com/time_series"
    params_price = {
        "symbol": symbole,
        "interval": "5min",
        "outputsize": 1,
        "apikey": api_key
    }

    # 📈 Récupération du RSI 14
    url_rsi = f"https://api.twelvedata.com/rsi"
    params_rsi = {
        "symbol": symbole,
        "interval": "5min",
        "time_period": 14,
        "apikey": api_key
    }

    # 📉 Récupération des moyennes mobiles
    url_ma50 = f"https://api.twelvedata.com/ma"
    url_ma200 = f"https://api.twelvedata.com/ma"
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
        ma50 = requests.get(url_ma50, params=params_ma50).json()
        ma200 = requests.get(url_ma200, params=params_ma200).json()

        if "values" not in prix:
            raise ValueError(f"❌ Erreur données prix : {prix}")
        candle = prix["values"][0]

        open_price = float(candle["open"])
        high_price = float(candle["high"])
        low_price = float(candle["low"])
        close_price = float(candle["close"])
        volume = candle.get("volume", "N/A")
        average_price = (high_price + low_price + close_price) / 3

        heure = datetime.datetime.now(pytz.timezone("Europe/Paris")).strftime("%Y-%m-%d %H:%M:%S")

        # RSI
        rsi_value = rsi["values"][0]["rsi"] if "values" in rsi else "N/A"

        # Moyennes mobiles
        ma_50 = float(ma50["values"][0]["ma"]) if "values" in ma50 else None
        ma_200 = float(ma200["values"][0]["ma"]) if "values" in ma200 else None
        tendance = "haussière" if ma_50 and ma_200 and ma_50 > ma_200 else "baissière" if ma_50 and ma_200 else "indéterminée"

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

        return heure, indicateurs

    except Exception as e:
        raise ValueError(f"❌ Erreur récupération {symbole} : {e}")
