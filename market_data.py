import yfinance as yf

def recuperer_donnees(actif):
    try:
        symboles_yf = {
            "XAUUSD": "GC=F",
            "NASDAQ": "^IXIC",
            "DAX": "^GDAXI"
        }

        symbole_yf = symboles_yf.get(actif)
        if not symbole_yf:
            raise ValueError(f"❌ Aucun symbole trouvé pour {actif}")

        data = yf.Ticker(symbole_yf).history(period="1d", interval="5m")
        if data.empty:
            raise ValueError(f"❌ Aucune donnée trouvée pour {actif}")

        dernier_prix = data["Close"].iloc[-1]

        return {
            "actif": actif,
            "prix": float(dernier_prix)
        }

    except Exception as e:
        raise ValueError(f"❌ Erreur lors de la récupération de {actif} : {e}")
