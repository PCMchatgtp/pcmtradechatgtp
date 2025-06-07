import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generer_signal_ia(symbole, donnees, heure, indicateurs):
    commentaire = f"Analyse IA pour {symbole} :\nVolume : {indicateurs['volume']}\nClôture : {indicateurs['close']}\nHeure : {heure}"
    plan = f"TRADE: {symbole} | Entrée : {indicateurs['close']} | Stop : {round(indicateurs['close'] - 1, 2)} | TP1 : {round(indicateurs['close'] + 1, 2)}"
    return plan, commentaire
