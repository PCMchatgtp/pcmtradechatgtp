import requests

def recuperer_donnees(symbole, api_key):
    url = f"https://api.twelvedata.com/time_series?symbol={symbole}&interval=5min&outputsize=30&apikey={api_key}"
    reponse = requests.get(url)
    data = reponse.json()

    if "values" not in data:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")

    return data["values"]