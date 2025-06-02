import yfinance as yf
import requests

def recuperer_donnees(actif: str):
    try:
        if actif == "XAUUSD":
            url = "https://api.forexrate.host/latest?base=USD&symbols=XAU"
            reponse = requests.get(url, timeout=10)
            data = reponse.json()

            if "rates" in data and "XAU" in data["rates"]:
                prix = 1 / data["rates"]["XAU"]
                return {
                    "actif": actif,
                    "prix": round(prix, 2),
                    "source": "forexrate.host"
                }
            else:
                raise ValueError(f"❌ Données invalides de forexrate.host : {data}")

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
