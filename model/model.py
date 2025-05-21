import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._bestPath = []
        self._bestPeso = 0

    def getAllYears(self):
        return DAO.getAllYears()

    def getAllNations(self):
        return DAO.getAllNations()

    def buildGraph(self, country, year):
        self._graph.clear()
        self._nodes = []
        nodes = DAO.getNodes(country)
        for n in nodes:
            self._nodes.append(n)
        self._graph.add_nodes_from(nodes)
        self._addEdges(year)
        return self._graph

    def _addEdges(self, year):
        for u in self._nodes:
            for v in self._nodes:
                if u.Retailer_code < v.Retailer_code:
                    peso = DAO.verificaNodi(u, v, year)
                    if peso is not None:
                        self._graph.add_edge(u, v, weight=peso)

    def getArchiIncidenti(self):
        diz = {}
        for n in self._nodes:
            somma = 0
            for edge in self._graph.edges(n, data=True):
                somma += int(edge[2]["weight"][0]["N"])
            diz[n] = somma
        chiaviOrdinate = sorted(diz, key=lambda n: diz[n], reverse=True)
        dizOrdinato = {}
        for a in chiaviOrdinate:
            dizOrdinato[a] = diz[a]
        return dizOrdinato

    def searchPath(self, N):
        self._bestPath = []
        self._bestPeso = 0
        for source in self._nodes:
            if source.Retailer_name=="SportsClub":
                pass
            self._startRecursion(source, N)

        return self._bestPath, self._bestPeso

    def _startRecursion(self, source, N):
        self._ricorsione([source], N, 0)

    def _ricorsione(self, parziale, archiTotali, peso):
        if len(parziale) == archiTotali + 1:  # condizione terminale
            if peso > self._bestPeso and parziale[0] != parziale[-1]:
                self._bestPath = copy.deepcopy(parziale)
                self._bestPeso = peso
            return
        else:
            for n in self._graph.neighbors(parziale[-1]):
                if n not in parziale:
                    peso += self._graph.get_edge_data(parziale[-1], n)['weight'][0]["N"]
                    #self._graph[1][2]["peso"]*********************
                    parziale.append(n)
                    self._ricorsione(parziale, archiTotali, peso)
                    parziale.pop()


    def _verificaParziale(self, parziale):
        if parziale[0] != parziale[-1]:
            return False
        for nodo in parziale:
            i = parziale.index(nodo)
            if nodo in parziale[:i] or nodo in parziale[i + 1:]:
                return False
        return True
