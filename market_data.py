import requests

def recuperer_donnees(symbole_twelve, twelve_data_api_key):
    url = f"https://api.twelvedata.com/time_series?symbol={symbole_twelve}&interval=5min&outputsize=2&apikey={twelve_data_api_key}"
    response = requests.get(url)
    data = response.json()

    if "values" not in data:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")

    cours = []
    for point in data["values"]:
        cours.append({
            "timestamp": point["datetime"],
            "open": float(point["open"]),
            "high": float(point["high"]),
            "low": float(point["low"]),
            "close": float(point["close"]),
            "volume": float(point["volume"]),
        })

    return cours

def analyser_tendance(cours):
    if len(cours) < 2:
        return "indécise"
    dernier_close = cours[0]["close"]
    précédent_close = cours[1]["close"]
    if dernier_close > précédent_close:
        return "haussière"
    elif dernier_close < précédent_close:
        return "baissière"
    else:
        return "indécise"
