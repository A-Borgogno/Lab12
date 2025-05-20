import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()

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
                somma += int(edge[2]["weight"])
            diz[n] = somma
        return diz
