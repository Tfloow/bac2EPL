def dijkstra(trajets, durees, voyage):
    graphe, destination, listLocation = creationGraphe(trajets, durees, voyage)
    trajet_min = [[] for _ in range(len(graphe))]
    duree_min = [float("inf") for _ in range(len(graphe))]
    duree_min[0] = 0
    destination = destination[-1]
    # trouve le point vers lequel on va

    # Fail proof
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

    # fais la conversion des numéros de noeuds en string 3 lettres
    resultat = "".join(f"{listLocation[node]}-" for node in trajet_min[destination])
    resultat += listLocation[destination]

    return (resultat, duree_min[destination])


def creationGraphe(trajets, durees, voyage):

    if(len(trajets) != len(durees)):
        raise IndexError("too much or too little journey for weights or vice versa")

    knownLocation = []
    new = [f.split("-") for f in trajets]
    Final = voyage.split("-")


    for g in new:
        for a in g:
            if (a not in knownLocation):
                knownLocation.append(a)

    # mets le noeud de départ à 0 et le noeud de fin à la fin
    knownLocation[knownLocation.index(Final[0])], knownLocation[0] = knownLocation[0], knownLocation[knownLocation.index(Final[0])]
    knownLocation[knownLocation.index(Final[-1])], knownLocation[-1] = knownLocation[-1], knownLocation[knownLocation.index(Final[-1])]

    #crée un dictionnaire représentant le graphe
    liaison = {f: [] for f in range(len(knownLocation))}
    for i, point in enumerate(new):
        liaison[knownLocation.index(point[0])].append((knownLocation.index(point[1]), durees[i]))
        liaison[knownLocation.index(point[1])].append((knownLocation.index(point[0]), durees[i]))


    return liaison, (knownLocation.index(Final[0]), knownLocation.index(Final[1])), knownLocation


voyage = "LUX-LIS"
trajets = ["BRU-PAR","BRU-LUX","PAR-LUX","LUX-STR","PAR-STR","PAR-LYO","STR-LYO","PAR-BOR","LYO-MAR","LYO-BAR", "BOR-MAR","BOR-BAR","BOR-MAD","MAR-BAR","BAR-MAD","MAD-POR","MAD-LIS","POR-LIS", "BRU-PAR"]
durees = [1,3,3,3,3,2,4,2,2,5,6,6,9,5,2,9,10,3,5]
print(dijkstra(trajets, durees, voyage))

voyage = "BRU-LIS"
trajets = ["BRU-LIS"]
durees = [3]
print(dijkstra(trajets, durees, voyage))

voyage = "BRU-LUX"
trajets = ["BRU-LIS"]
durees = [3]
print(dijkstra(trajets, durees, voyage))