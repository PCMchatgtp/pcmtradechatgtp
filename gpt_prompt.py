def generer_signal_ia(donnees, contexte_macro):
    prix = donnees["prix"]
    actif = donnees["actif"]

    stop = round(prix * 0.995, 2)
    tp1 = round(prix * 1.01, 2)
    tp2 = round(prix * 1.02, 2)
    tp3 = round(prix * 1.03, 2)

    return {
        "actif": actif,
        "prix": prix,
        "macro": contexte_macro.get("résumé", "Données macro indisponibles"),
        "entree": prix,
        "stop": stop,
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3
    }
