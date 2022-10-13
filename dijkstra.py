import time


def dijkstra(trajets, durees, voyage):
    graphe, destination, listLocation = creationGraphe(trajets, durees, voyage)
    trajet_min = [[] for _ in range(len(graphe))]
    duree_min = [float("inf") for _ in range(len(graphe))]
    duree_min[0] = 0
    destination = destination[-1]
    print(graphe)

    # trouve le point vers lequel on va



    ending = False
    for node in graphe.keys():
        if node == list(graphe.keys())[-1]:
            ending = True
        for connection in graphe[node]:
            if ending and duree_min[node] > duree_min[connection[0]] + connection[-1]:
                duree_min[node] = connection[-1] + duree_min[connection[0]]
                trajet_min[node].clear()
                for prevNode in trajet_min[connection[0]]:
                    trajet_min[node].append(prevNode)
                trajet_min[node].append(connection[0])
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
    Final = voyage.split("-")

    return liaison, (knownLocation.index(Final[0]), knownLocation.index(Final[1])), knownLocation


voyage = "BRU-LIS"
trajets = ["BRU-PAR","BRU-LUX","PAR-LUX","LUX-STR","PAR-STR","PAR-LYO","STR-LYO","PAR-BOR","LYO-MAR","LYO-BAR", "BOR-MAR","BOR-BAR","BOR-MAD","MAR-BAR","BAR-MAD","MAD-POR","MAD-LIS","POR-LIS", "BRU-PAR"]
durees = [1,3,3,3,3,2,4,2,2,5,6,6,9,5,2,9,10,3,5]
for jqmfj in range(20):
    timing = time.time_ns()
    time.sleep(1)
    print(dijkstra(trajets,durees, voyage), time.time_ns()-timing)
