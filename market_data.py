import requests
import datetime
import pytz
import time
from config import OPENAI_API_KEY

_cache = {}

def recuperer_donnees(symbole, api_key):
    now = time.time()

    if symbole in _cache and now - _cache[symbole]["timestamp"] < 300:
        return _cache[symbole]["heure"], _cache[symbole]["indicateurs"]

    url_base = "https://api.twelvedata.com/"
    params_base = {
        "symbol": symbole,
        "interval": "5min",
        "apikey": api_key
    }

    endpoints = {
        "prix": ("time_series", {"outputsize": 1}),
        "rsi": ("rsi", {"time_period": 14}),
        "ma50": ("ma", {"time_period": 50}),
        "ma200": ("ma", {"time_period": 200}),
        "ema9": ("ema", {"time_period": 9}),
        "macd": ("macd", {"short_period": 12, "long_period": 26, "signal_period": 9}),
        "stoch": ("stoch", {"slow_k_period": 14, "slow_d_period": 3}),
        "bbands": ("bbands", {"time_period": 20})
    }

    data = {}

    try:
        for key, (endpoint, extra_params) in endpoints.items():
            params = params_base.copy()
            params.update(extra_params)
            response = requests.get(url_base + endpoint, params=params).json()
            data[key] = response

        if "values" not in data["prix"]:
            raise ValueError(f"❌ Erreur données prix : {data['prix']}")
        candle = data["prix"]["values"][0]

        open_price = float(candle["open"])
        high_price = float(candle["high"])
        low_price = float(candle["low"])
        close_price = float(candle["close"])
        volume = candle.get("volume", "N/A")
        average_price = (high_price + low_price + close_price) / 3

        heure = datetime.datetime.now(pytz.timezone("Europe/Paris")).strftime("%Y-%m-%d %H:%M:%S")

        rsi_value = data["rsi"]["values"][0]["rsi"] if "values" in data["rsi"] else "N/A"
        ma_50 = float(data["ma50"]["values"][0]["ma"]) if "values" in data["ma50"] else None
        ma_200 = float(data["ma200"]["values"][0]["ma"]) if "values" in data["ma200"] else None
        ema_9 = float(data["ema9"]["values"][0]["ema"]) if "values" in data["ema9"] else None
        macd_line = data["macd"]["values"][0]["macd"] if "values" in data["macd"] else "N/A"
        macd_signal = data["macd"]["values"][0]["signal"] if "values" in data["macd"] else "N/A"
        stoch_k = data["stoch"]["values"][0]["slow_k"] if "values" in data["stoch"] else "N/A"
        stoch_d = data["stoch"]["values"][0]["slow_d"] if "values" in data["stoch"] else "N/A"
        bb_upper = data["bbands"]["values"][0]["upper_band"] if "values" in data["bbands"] else "N/A"
        bb_lower = data["bbands"]["values"][0]["lower_band"] if "values" in data["bbands"] else "N/A"

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
            f"MACD : {macd_line} | Signal : {macd_signal}\n"
            f"STOCH %K : {stoch_k} | %D : {stoch_d}\n"
            f"Bollinger Haut : {bb_upper} | Bas : {bb_lower}\n"
            f"EMA9 : {ema_9}\n"
            f"Tendance : {tendance}\n"
            f"Variation % : {((close_price - open_price) / open_price * 100):.2f}%"
        )

        _cache[symbole] = {
            "timestamp": now,
            "heure": heure,
            "indicateurs": indicateurs
        }

        return heure, indicateurs

    except Exception as e:
        raise ValueError(f"❌ Erreur récupération {symbole} : {e}")
