import requests
import datetime

def recuperer_donnees(symbole, twelve_data_api_key):
    url = f"https://api.twelvedata.com/time_series?symbol={symbole}&interval=5min&apikey={twelve_data_api_key}&outputsize=2"
    response = requests.get(url)
    data = response.json()

    if "status" in data and data["status"] == "error":
        raise ValueError(f"❌ Données invalides de TwelveData pour {symbole} : {data}")

    try:
        dernier_cours = float(data["values"][0]["close"])
        precedent_cours = float(data["values"][1]["close"])
        return {"prix": dernier_cours, "precedent": precedent_cours}
    except Exception as e:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {e}")

def analyser_tendance(donnees):
    prix = donnees["prix"]
    precedent = donnees["precedent"]
    if prix > precedent:
        return "hausse"
    elif prix < precedent:
        return "baisse"
    else:
        return "neutre"
