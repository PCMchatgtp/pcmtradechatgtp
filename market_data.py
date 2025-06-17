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

    base_url = "https://api.twelvedata.com"

    def get(endpoint, params):
        try:
            response = requests.get(f"{base_url}/{endpoint}", params={**params, "symbol": symbole, "interval": "5min", "apikey": api_key})
            data = response.json()
            if "values" in data and isinstance(data["values"], list) and data["values"]:
                return data["values"][0]
            elif "value" in data:
                return data  # ex: VWAP
            else:
                raise ValueError(f"⚠️ Données manquantes pour {endpoint}")
        except Exception as e:
            print(f"❌ Erreur API {endpoint} pour {symbole} : {e}")
            return {}

    try:
        candle = get("time_series", {"outputsize": 1})
        if not candle:
            raise ValueError("❌ Bougie manquante")

        open_price = float(candle.get("open", 0))
        high_price = float(candle.get("high", 0))
        low_price = float(candle.get("low", 0))
        close_price = float(candle.get("close", 0))

        # 🚫 Si le prix est manifestement incorrect (ex : < 10), on stoppe tout
        if close_price < 100:
            raise ValueError(f"❌ Données incohérentes : close_price = {close_price}")

        rsi = get("rsi", {"time_period": 14})
        ma50 = get("ma", {"time_period": 50})
        ma200 = get("ma", {"time_period": 200})
        macd = get("macd", {"fast_period": 12, "slow_period": 26, "signal_period": 9})
        bbands = get("bbands", {"time_period": 20, "stddev": 2})
        vwap = get("vwap", {})

        volume = candle.get("volume", "N/A")
        average_price = (high_price + low_price + close_price) / 3
        heure = datetime.datetime.now(pytz.timezone("Europe/Paris")).strftime("%Y-%m-%d %H:%M:%S")

        rsi_value = rsi.get("rsi", "N/A")
        ma_50 = float(ma50.get("ma")) if "ma" in ma50 else None
        ma_200 = float(ma200.get("ma")) if "ma" in ma200 else None
        tendance = "haussière" if ma_50 and ma_200 and ma_50 > ma_200 else "baissière" if ma_50 and ma_200 else "indéterminée"

        macd_val = macd.get("macd", "N/A")
        signal_val = macd.get("signal", "N/A")
        bb_upper = bbands.get("upper_band", "N/A")
        bb_middle = bbands.get("middle_band", "N/A")
        bb_lower = bbands.get("lower_band", "N/A")
        vwap_val = vwap.get("value", "N/A")  # la clé est "value" pour VWAP

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
            f"Variation % : {((close_price - open_price) / open_price * 100):.2f}%\n"
            f"MACD : {macd_val}\n"
            f"Signal : {signal_val}\n"
            f"Bollinger Haut : {bb_upper}\n"
            f"Bollinger Milieu : {bb_middle}\n"
            f"Bollinger Bas : {bb_lower}\n"
            f"VWAP : {vwap_val}"
        )

        _cache[symbole] = {
            "timestamp": now,
            "heure": heure,
            "indicateurs": indicateurs
        }

        return heure, indicateurs

    except Exception as e:
        raise ValueError(f"❌ Erreur récupération {symbole} : {e}")
