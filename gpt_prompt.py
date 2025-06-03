def generer_signal_ia(donnees, contexte_macro):
    prix = donnees["prix"]
    actif = donnees["actif"]

    # TP et SL basés sur une stratégie simple pour démo
    stop = round(prix - (prix * 0.005), 2)
    tp1 = round(prix + (prix - stop), 2)
    tp2 = round(tp1 + (tp1 - prix), 2)
    tp3 = round(tp2 + (tp1 - prix), 2)

    return {
        "actif": actif,
        "prix": prix,
        "stop": stop,
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3,
        "break_even": "🎯 Break-even après TP1 atteint.",
        "macro": contexte_macro.get("résumé", "Macro inconnue")
    }
