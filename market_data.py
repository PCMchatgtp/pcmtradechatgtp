import requests

def recuperer_donnees(symbole, api_key):
    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbole,
        "interval": "5min",
        "outputsize": 5,
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "values" not in data:
        raise ValueError(f"❌ Erreur lors de l'extraction des cours : {data}")

    donnees = data["values"]

    # Indicateurs simples
    volumes = [float(candle["volume"]) for candle in donnees if "volume" in candle]
    close_prices = [float(candle["close"]) for candle in donnees]

    indicateurs = {
        "volume_moyen": sum(volumes) / len(volumes) if volumes else 0,
        "close_moyenne": sum(close_prices) / len(close_prices) if close_prices else 0
    }

    return donnees, indicateurs