import requests
from datetime import datetime, timedelta

def contexte_macro_simplifie():
    try:
        # On récupère les événements du jour depuis Forex Factory (non officiel)
        aujourdhui = datetime.utcnow().date().isoformat()
        url = f"https://cdn-nfs.forexfactory.net/calendar/events/{aujourdhui}.json"
        reponse = requests.get(url, timeout=10)
        data = reponse.json()

        evenements = data.get("events", [])
        if not isinstance(evenements, list):
            return "❌ Format de données macro non valide."

        result = ""
        for event in evenements:
            if not isinstance(event, dict):
                continue  # Ignore les erreurs de type

            importance = event.get("importance", "")
            if importance.lower() in ["high", "medium"]:
                title = event.get("title", "Événement inconnu")
                actual = event.get("actual", "N/A")
                previous = event.get("previous", "N/A")
                forecast = event.get("forecast", "N/A")

                result += (
                    f"- {title} ({importance}) : Actuel {actual}, "
                    f"Précédent {previous}, Prévision {forecast}\n"
                )

        return result if result else "✅ Aucun événement macroéconomique majeur aujourd’hui."

    except Exception as e:
        return f"❌ Erreur macro API : {e}"
