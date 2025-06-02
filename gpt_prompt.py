def generer_signal_ia(donnees, contexte, actif):
    dernier_prix = donnees["c"][-1]

    return f"""
📊 Analyse IA
Actif : {actif}
Prix actuel : {dernier_prix}
Contexte macro : {contexte}

🔁 Entrée : {dernier_prix}
📉 Stop : {round(dernier_prix * 0.995, 2)}
📈 TP1 : {round(dernier_prix * 1.01, 2)}
📈 TP2 : {round(dernier_prix * 1.02, 2)}
📈 TP3 : {round(dernier_prix * 1.03, 2)}
🎯 Break-even après TP1 atteint.
"""
