import requests
import os

API_KEY_TWELVE = os.environ.get("TWELVE_API_KEY")

def recuperer_donnees(actif):
    symboles = {
        "XAUUSD": "XAU/USD",
        "BTCUSD": "BTC/USD",
        "NASDAQ": "QQQ"
    }

    symbole = symboles.get(actif)
    if not symbole:
        raise ValueError(f"❌ Symbole introuvable pour {actif}")

    url = f"https://api.twelvedata.com/time_series?symbol={symbole}&interval=5min&apikey={API_KEY_TWELVE}&outputsize=2"

    r = requests.get(url)
    data = r.json()

    if "status" in data and data["status"] == "error":
        raise ValueError(f"❌ Données invalides de TwelveData pour {actif} : {data}")

    try:
        close_prices = [float(i["close"]) for i in data["values"][:2]]
        variation = close_prices[0] - close_prices[1]
        direction = "hausse" if variation > 0 else "baisse"
        return {
            "actif": actif,
            "prix": close_prices[0],
            "variation": round(variation, 2),
            "direction": direction
        }
    except Exception as e:
        raise ValueError(f"❌ Erreur lors de l’analyse des données de {actif} : {e}")

def analyser_tendance(donnees):
    variation = donnees.get("variation", 0)
    direction = donnees.get("direction", "indéterminée")

    if abs(variation) < 0.1:
        return "neutre"
    return direction
