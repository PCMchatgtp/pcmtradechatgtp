import requests
from config import FINNHUB_API_KEY

def recuperer_donnees(actif):
    if actif == "XAUUSD":
        # Source gratuite sans clé API
        url = "https://api.forexrate.host/latest?base=USD&symbols=XAU"
        response = requests.get(url)
        data = response.json()

        if "rates" not in data or "XAU" not in data["rates"]:
            raise ValueError("❌ API ForexRateHost ne retourne pas de prix pour l'or")

        prix_usd = 1 / data["rates"]["XAU"]  # 1 once d’or = xxx USD
        return {"c": [prix_usd] * 100}  # On duplique artificiellement pour simuler 100 bougies

    # Symboles Finnhub pour autres actifs
    symbol_map = {
        "DAX": "INDEX:DEU40",
        "NASDAQ": "US:NDX"
    }

    symbol = symbol_map.get(actif)
    if not symbol:
        raise ValueError(f"❌ Symbole inconnu pour l’actif {actif}")

    url = f"https://finnhub.io/api/v1/index/candle?symbol={symbol}&resolution=5&count=100&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get("s") != "ok":
        raise ValueError(f"❌ API Finnhub n’a pas retourné de données valides pour {actif}")

    return data  # Contient 'c', 'o', 'h', 'l', 't', 's'
