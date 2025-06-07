import requests

def recuperer_donnees(symbole, api_key):
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbole,
        "interval": "5min",
        "outputsize": 10,
        "apikey": api_key
    }
    reponse = requests.get(url, params=params)
    data = reponse.json()

    if "values" not in data:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")

    valeurs = data["values"]
    derniers_cours = valeurs[0]
    indicateurs = {
        "close": [float(v["close"]) for v in valeurs],
        "volume": [float(v["volume"]) for v in valeurs],
    }

    return derniers_cours, indicateurs