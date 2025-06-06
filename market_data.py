import requests

def recuperer_donnees(symbole, twelve_data_api_key):
    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbole,
        "interval": "5min",
        "outputsize": 30,
        "apikey": twelve_data_api_key,
        "format": "JSON"
    }

    reponse = requests.get(url, params=params)
    data = reponse.json()

    if "values" not in data:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")

    cours = [
        {
            "datetime": point["datetime"],
            "open": float(point["open"]),
            "high": float(point["high"]),
            "low": float(point["low"]),
            "close": float(point["close"]),
            "volume": float(point.get("volume", 0))
        }
        for point in data["values"]
    ]

    return cours
