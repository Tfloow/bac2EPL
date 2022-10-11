import time

def djikstra(trajets, durees, voyage):
    graphe, destination, listLocation = creationGraphe(trajets, durees, voyage)
    trajet_min = [[] for _ in range(len(graphe))]
    duree_min = [float("inf") for _ in range(len(graphe))]
    duree_min[0] = 0
    print(graphe)

    # trouve le point vers lequel on va
    for finaldestination in destination:
        if finaldestination != 0:
            destination = finaldestination
            break

    for node in graphe.keys():
        for connection in graphe[node]:
            if duree_min[connection[0]] > connection[-1] + duree_min[node]:
                duree_min[connection[0]] = connection[-1] + duree_min[node]
                trajet_min[connection[0]].clear()
                for prevNode in trajet_min[node]:
                    trajet_min[connection[0]].append(prevNode)
                trajet_min[connection[0]].append(node)

    # faise la conversion des numéros de noeuds en string 3 lettres
    resultat = "".join(f"{listLocation[node]}-" for node in trajet_min[destination])
    resultat += listLocation[destination]

    return (resultat, duree_min[destination])


def creationGraphe(trajets, durees, voyage):
    knownLocation = []
    new = [f.split("-") for f in trajets]
    for g in new:
        for a in g:
            if (a not in knownLocation):
                knownLocation.append(a)

    liaison = {f: [] for f in range(len(knownLocation))}
    for i, point in enumerate(new):
        liaison[knownLocation.index(point[0])].append((knownLocation.index(point[1]), durees[i]))
        liaison[knownLocation.index(point[1])].append((knownLocation.index(point[0]), durees[i]))
    Final = voyage[0].split("-")

    return liaison, (knownLocation.index(Final[0]), knownLocation.index(Final[1])), knownLocation


