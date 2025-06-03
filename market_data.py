import yfinance as yf
from config import SYMBOLS

def recuperer_donnees(actif):
    try:
        symbole = SYMBOLS.get(actif)
        if not symbole:
            raise ValueError(f"Symbole non trouvé pour l'actif : {actif}")
        data = yf.Ticker(symbole).history(period="1d", interval="5m")
        if data.empty:
            raise ValueError(f"Données vides pour {actif}")
        prix = round(data["Close"].iloc[-1], 2)
        return {
            "actif": actif,
            "prix": prix
        }
    except Exception as e:
        raise ValueError(f"❌ Erreur lors de la récupération de {actif} : {e}")
