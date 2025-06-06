def analyser_tendance(cours):
    """
    Analyse simple de la tendance sur les 10 dernières bougies :
    - retourne 'hausse' si majorité de hausses
    - 'baisse' si majorité de baisses
    - sinon 'indécise'
    """
    if not cours or len(cours) < 2:
        return "indécise"

    hausses = 0
    baisses = 0

    for i in range(1, len(cours)):
        if cours[i]["close"] > cours[i-1]["close"]:
            hausses += 1
        elif cours[i]["close"] < cours[i-1]["close"]:
            baisses += 1

    if hausses > baisses:
        return "hausse"
    elif baisses > hausses:
        return "baisse"
    else:
        return "indécise"
