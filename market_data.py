import yfinance as yf
from config import SYMBOLS

def recuperer_donnees(actif):
    try:
        symbole = SYMBOLS[actif]
        data = yf.Ticker(symbole).history(period="1d", interval="5m")
        if data.empty:
            raise ValueError(f"Données introuvables pour {actif}")

        dernier_prix = round(data["Close"].iloc[-1], 2)

        return {
            "actif": actif,
            "symbole": symbole,
            "prix": dernier_prix,
        }

    except Exception as e:
        raise ValueError(f"❌ Erreur lors de la récupération de {actif} : {e}")
