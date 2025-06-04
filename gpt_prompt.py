import openai

def generer_signal_ia(donnees, contexte_macro):
    prompt = f"""
Tu es un expert en trading scalping. Analyse les données suivantes et détermine s'il y a une opportunité de trade.

Actif : {donnees['actif']}
Prix actuel : {donnees['prix']}
Heure : {donnees['heure']}
Contexte macroéconomique : {contexte_macro}

Donne ta réponse sous forme d’un dictionnaire JSON contenant :
- tendance (achat ou vente ou neutre)
- entree (prix d’entrée)
- stop
- tp1
- tp2
- tp3

Si aucune opportunité, répond : "neutre".
"""

    reponse = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    contenu = reponse["choices"][0]["message"]["content"]

    if contenu.strip().lower() == "neutre":
        return {"tendance": "neutre"}

    try:
        resultat = eval(contenu)
        return resultat
    except:
        raise ValueError("❌ Réponse IA invalide ou mal formée :\n" + contenu)
