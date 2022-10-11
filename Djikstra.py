import time

def dijkstra(trajets, durees, voyage):
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


trajets = ["LIS-POR", "LIS-MAD", "POR-MAD", "MAD-BAR", "MAD-BOR", "BAR-BOR", "BAR-MAR", "BAR-LYO", "BOR-PAR", "PAR-BRU"
    , "BRU-LUX", "PAR-LUX", "LUX-STR", "PAR-STR", "STR-LYO", "MAR-LYO", "PAR-LYO"]
durees = [3, 10, 9, 2, 9, 6, 5, 5, 2, 1, 3, 3, 3, 3, 4, 2, 2]
startTime = time.time()
print(startTime)
print(dijkstra(trajets, durees, ["BRU-LIS"]))
print(time.sleep(1))
print(time.time())
print(time.time()-startTime)
