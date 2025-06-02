def generer_signal_ia(donnees, contexte):
    actif = donnees["actif"]
    prix = donnees["prix"]

    # Exemple simplifié pour XAUUSD
    if actif == "XAUUSD":
        stop = round(prix - 16, 1)
        tp1 = round(prix + 33, 1)
        tp2 = round(prix + 67, 1)
        tp3 = round(prix + 101, 1)
    else:
        stop = round(prix - 50, 1)
        tp1 = round(prix + 100, 1)
        tp2 = round(prix + 200, 1)
        tp3 = round(prix + 300, 1)

    return {
        "actif": actif,
        "prix": prix,
        "entree": prix,
        "stop": stop,
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3,
        "break_even": True
    }
