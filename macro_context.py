import requests
import datetime
import os

def contexte_macro_simplifie():
    try:
        # Utilisation de l’API gratuite de ForexFactory (via scraping simplifié)
        today = datetime.date.today().strftime("%Y-%m-%d")
        url = f"https://cdn-nfs.forexfactory.net/calendar/events/{today}.json"

        response = requests.get(url)
        data = response.json()

        # On filtre uniquement les événements importants
        evenements_importants = []
        for event in data:
            if isinstance(event, dict):
                importance = event.get("importance", "").lower()
                if "high" in importance:
                    evenements_importants.append(f"{event.get('title', 'Événement inconnu')} à {event.get('time', '?')}")

        if not evenements_importants:
            return "Pas d’événements macro importants aujourd’hui."

        # On résume
        resume = "Événements macro importants aujourd’hui :\n" + "\n".join(evenements_importants)
        return resume

    except Exception as e:
        return f"❌ Erreur macro API : {e}"
