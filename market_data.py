import requests
from config import OPENAI_API_KEY

def recuperer_donnees(symbole):
    # Ceci est un exemple factice, remplacer avec votre appel réel à Twelve Data
    response = requests.get(f"https://api.twelvedata.com/time_series?symbol={symbole}&interval=5min&apikey={OPENAI_API_KEY}")
    data = response.json()

    if 'values' not in data:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")

    values = data['values']
    heure = values[0]['datetime']
    indicateurs = {"volume": values[0].get("volume", "N/A")}

    return values, heure, indicateurs