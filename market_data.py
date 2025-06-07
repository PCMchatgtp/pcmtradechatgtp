import requests

def recuperer_donnees(symbole):
    url = f"https://api.twelvedata.com/time_series?symbol={symbole}&interval=5min&outputsize=20&apikey={API_KEY}"
    reponse = requests.get(url)
    data = reponse.json()
    if "values" not in data:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")
    valeurs = data["values"]
    heure = valeurs[0]["datetime"]
    indicateurs = {
        "volume": float(valeurs[0]["volume"]),
        "close": float(valeurs[0]["close"]),
    }
    return valeurs, heure, indicateurs
