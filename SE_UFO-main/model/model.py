import copy

from geopy import distance

from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.lista_anni = []
        self.lista_forme = []
        self.g = nx.Graph()
        self.dizionario_stati = {}

    def get_years(self):
        self.lista_anni = DAO.get_years()

    def get_shapes(self):
        self.lista_forme = DAO.get_shapes()

    def get_stati(self):
        self.lista_stati = DAO.get_stati()

        for stato in self.lista_stati:
            self.dizionario_stati[stato.id] = stato

    def build_graph(self, year, shape):
        self.g.clear()

        self.get_stati()
        self.g.add_nodes_from(self.lista_stati)
        lista_archi = DAO.get_edges(year, shape)

        for arco in lista_archi: # arco = [id_st1, id_st2, weight]
            stato_1 = self.dizionario_stati[arco[0]]
            stato_2 = self.dizionario_stati[arco[1]]
            self.g.add_edge(stato_1, stato_2,weight=float(arco[2]))

        print(self.g)

        self.calcola_pesi_archi()

    def calcola_pesi_archi(self):

        self.lista_res = []
        lista = [] # nodo - somma_pesi

        for nodo in self.g.nodes():
            lista = [nodo,0.0]
            for neighbor in self.g.neighbors(nodo):
                lista[1] += self.g[nodo][neighbor]['weight']
            self.lista_res.append(lista)

    def compute_path(self):
        self.path = []
        self.path_edge = []
        self.sol_best = 0

        partial = []
        for n in self.g.nodes():
            partial.clear()
            partial.append(n)
            self._ricorsione(partial, [])

        print(self.path)
        print(self.path_edge)
        print(self.sol_best)

    def _ricorsione(self, partial, partial_edge):
        n_last = partial[-1]

        neighbors = self.get_admissible_neighbs(n_last, partial_edge)

        if len(neighbors) == 0:
            weight_path = self.compute_weight_path(partial_edge)
            if weight_path > self.sol_best:
                self.sol_best = weight_path + 0.0
                self.path = partial[:]
                self.path_edge = partial_edge[:]
            return

        for n in neighbors:
            partial_edge.append((n_last, n, self.g.get_edge_data(n_last, n)['weight']))
            partial.append(n)

            self._ricorsione(partial, partial_edge)

            partial.pop()
            partial_edge.pop()

    def get_admissible_neighbs(self, n_last, partial_edges):
        all_neigh = self.g.edges(n_last, data=True)
        result = []
        for e in all_neigh:
            if len(partial_edges) != 0:
                if e[2]["weight"] > partial_edges[-1][2]:
                    result.append(e[1])
            else:
                result.append(e[1])
        return result

    def compute_weight_path(self, mylist):
        weight = 0
        for e in mylist:
            weight += distance.geodesic((e[0].lat, e[0].lng),
                                        (e[1].lat, e[1].lng)).km
        return weight

    def get_distance_weight(self, e):
        return distance.geodesic((e[0].lat, e[0].lng),
                                 (e[1].lat, e[1].lng)).km