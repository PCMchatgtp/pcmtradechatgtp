def generer_signal_ia(donnees, contexte_macro):
    prix = donnees["prix"]
    actif = donnees["actif"]

    tp1 = round(prix * 1.01, 2)
    tp2 = round(prix * 1.02, 2)
    tp3 = round(prix * 1.03, 2)
    stop = round(prix * 0.995, 2)

    return f'''
📡 Signal pour {actif} :

📊 Analyse IA
Actif : {actif}
Prix actuel : {prix}
Contexte macro : {contexte_macro.get("résumé", "Données indisponibles")}

🔁 Entrée : {prix}
📉 Stop : {stop}
📈 TP1 : {tp1}
📈 TP2 : {tp2}
📈 TP3 : {tp3}
🎯 Break-even après TP1 atteint.
'''
