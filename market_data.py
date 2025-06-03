# market_data.py

import yfinance as yf

SYMBOL_MAPPING = {
    "XAUUSD": "GLD",       # Gold via SPDR Gold ETF
    "DAX": "EWG",          # Allemagne via iShares MSCI Germany ETF
    "NASDAQ": "QQQ"        # Nasdaq via Invesco QQQ Trust
}

def recuperer_donnees(actif: str) -> dict:
    symbole_yahoo = SYMBOL_MAPPING.get(actif)
    if not symbole_yahoo:
        raise ValueError(f"❌ Symbole introuvable pour {actif}")

    try:
        ticker = yf.Ticker(symbole_yahoo)
        data = ticker.history(period="1d", interval="5m")

        if data.empty:
            raise ValueError(f"❌ Aucune donnée trouvée pour {symbole_yahoo} sur Yahoo Finance.")

        dernier_prix = round(data["Close"].iloc[-1], 2)
        return {
            "actif": actif,
            "prix": dernier_prix
        }
    except Exception as e:
        raise ValueError(f"❌ Erreur lors de la récupération de {actif} ({symbole_yahoo}) : {e}")
