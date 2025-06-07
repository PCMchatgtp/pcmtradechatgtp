
import requests

def recuperer_donnees(symbole, api_key):
    url = f"https://api.twelvedata.com/time_series?symbol={symbole}&interval=5min&outputsize=12&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if 'status' in data and data['status'] == 'error':
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")

    values = data.get("values")
    if not values:
        raise ValueError("❌ Erreur : données de marché manquantes ou invalides.")

    dernier = values[0]
    precedent = values[1]

    prix_actuel = float(dernier['close'])
    prix_precedent = float(precedent['close'])

    variation = prix_actuel - prix_precedent
    direction = "hausse" if variation > 0 else "baisse" if variation < 0 else "neutre"

    indicateurs = {
        "prix_actuel": prix_actuel,
        "variation": variation,
        "direction": direction,
        "volume": float(dernier['volume']) if 'volume' in dernier else None
    }

    return indicateurs
