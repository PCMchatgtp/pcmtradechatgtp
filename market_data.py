import requests
from config import TWELVEDATA_API_KEY

def recuperer_donnees(actif):
    symboles_twelve = {
        "XAUUSD": "XAU/USD",
        "NASDAQ": "NDX"
    }

    symbole = symboles_twelve.get(actif)
    if not symbole:
        raise ValueError(f"❌ Actif non supporté : {actif}")

    url = f"https://api.twelvedata.com/price?symbol={symbole}&apikey={TWELVEDATA_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        if "price" not in data:
            raise ValueError(f"❌ Données invalides de TwelveData pour {actif} : {data}")

        return {
            "actif": actif,
            "prix": float(data["price"])
        }

    except Exception as e:
        raise ValueError(f"❌ Erreur lors de la récupération de {actif} : {e}")
