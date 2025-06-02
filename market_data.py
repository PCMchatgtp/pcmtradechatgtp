import yfinance as yf
import requests
import os

def recuperer_donnees(actif: str):
    try:
        if actif == "XAUUSD":
            api_key = os.getenv("GOLD_API_KEY")
            url = "https://www.goldapi.io/api/XAU/USD"
            headers = {
                "x-access-token": api_key,
                "Content-Type": "application/json"
            }
            reponse = requests.get(url, headers=headers, timeout=10)
            data = reponse.json()

            if "price" not in data:
                raise ValueError(f"❌ Données invalides de GoldAPI : {data}")

            prix = data["price"]
            return {
                "actif": actif,
                "prix": round(prix, 2),
                "source": "goldapi"
            }

        elif actif == "DAX":
            ticker = "^GDAXI"
        elif actif == "NASDAQ":
            ticker = "^IXIC"
        else:
            raise ValueError(f"❌ Actif non supporté : {actif}")

        data = yf.download(ticker, period="1d", interval="5m", progress=False)

        if data.empty:
            raise ValueError(f"❌ yfinance n'a pas retourné de données pour {actif}")

        dernier_prix = round(data["Close"].iloc[-1], 2)

        return {
            "actif": actif,
            "prix": dernier_prix,
            "source": "yfinance"
        }

    except Exception as e:
        raise ValueError(f"❌ Erreur lors de la récupération de {actif} : {e}")
