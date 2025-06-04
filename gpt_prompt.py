def generer_signal_ia(donnees):
    prix = donnees["prix"]
    entrée = prix
    stop = round(prix * 0.995, 2)
    tp1 = round(prix * 1.01, 2)
    tp2 = round(prix * 1.02, 2)
    tp3 = round(prix * 1.03, 2)
    return {
        "entrée": entrée,
        "stop": stop,
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3
    }