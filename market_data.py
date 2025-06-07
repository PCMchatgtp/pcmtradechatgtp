import requests

def recuperer_donnees(symbol, api_key):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=5min&outputsize=1&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if "values" not in data:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")
    return data["values"][0]