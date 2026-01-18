import copy

import networkx as nx
from database.dao import DAO
from operator import itemgetter

class Model:
    def __init__(self):
        self.lista_categorie = []
        self.lista_prodotti = []
        self.dizionario_prodotti = {}
        self.g = nx.DiGraph()

    def get_date_range(self):
        return DAO.get_date_range()

    def get_categories(self):
        self.lista_categorie = DAO.get_categories()

    def get_products(self, id_categoria):
        self.lista_prodotti = DAO.get_products(id_categoria)
        for prodotto in self.lista_prodotti:
            self.dizionario_prodotti[int(prodotto.id)] = prodotto

        #print(self.lista_prodotti)

    def get_prodotti_venduti(self, id_categoria, data_inizio, data_fine):
        self.lista_tuple = DAO.get_prodotti_venduti(id_categoria, data_inizio, data_fine)
        self.dizionario_prodotti_venduti = {}

        for tupla in self.lista_tuple:
            self.dizionario_prodotti_venduti[int(tupla[0])] = int(tupla[1]) #{id_prodotto:numero_vendite}

        self.lista_id_prodotti_validi = []

        for key in self.dizionario_prodotti_venduti:
            self.lista_id_prodotti_validi.append(key)

    def build_graph(self):

        self.g.clear()

        self.g.add_nodes_from(self.lista_prodotti)

        for nodo1 in self.g.nodes():
            for nodo2 in self.g.nodes():

                if nodo1 == nodo2:
                    pass

                elif nodo1.id in self.lista_id_prodotti_validi and nodo2.id in self.lista_id_prodotti_validi:

                    if self.dizionario_prodotti_venduti[nodo1.id] > self.dizionario_prodotti_venduti[nodo2.id]:
                        self.g.add_edge(nodo1, nodo2, weight=self.dizionario_prodotti_venduti[nodo1.id]+self.dizionario_prodotti_venduti[nodo2.id])

                    elif self.dizionario_prodotti_venduti[nodo1.id] < self.dizionario_prodotti_venduti[nodo2.id]:
                        self.g.add_edge(nodo2, nodo1, weight=self.dizionario_prodotti_venduti[nodo1.id]+self.dizionario_prodotti_venduti[nodo2.id])

                    elif self.dizionario_prodotti_venduti[nodo1.id] == self.dizionario_prodotti_venduti[nodo2.id]:
                        self.g.add_edge(nodo1, nodo2, weight=self.dizionario_prodotti_venduti[nodo1.id]+self.dizionario_prodotti_venduti[nodo2.id])
                        self.g.add_edge(nodo2, nodo1, weight=self.dizionario_prodotti_venduti[nodo1.id] + self.dizionario_prodotti_venduti[nodo2.id])

        print(self.g)

    def get_prodotti_migliori(self):

        lista_dizionari_prodotti = []
        dizionario_prodotto = {"prodotto": None, "somma": None}

        for nodo in self.g.nodes():

            dizionario_prodotto = {"prodotto": None, "somma": 0.0}

            dizionario_prodotto["prodotto"] = nodo
            for edge in self.g.in_edges(nodo, data=True):
                dizionario_prodotto["somma"] -= edge[2]["weight"]
            for edge in self.g.out_edges(nodo, data=True):
                dizionario_prodotto["somma"] += edge[2]["weight"]
            lista_dizionari_prodotti.append(dizionario_prodotto)

        self.lista_ordinata = sorted(lista_dizionari_prodotti,key=itemgetter('somma'), reverse=True)

    def cerca_cammino(self, id_iniziale, id_finale, lunghezza_cammino):

        nodo_iniziale = self.dizionario_prodotti[id_iniziale]
        nodo_finale = self.dizionario_prodotti[id_finale]

        self.percorso_ottimo = []
        self.peso_ottimo = 0.0

        percorso_parziale = [nodo_iniziale]
        peso_parziale = 0.0

        self.ricorsione(percorso_parziale, nodo_finale,peso_parziale, lunghezza_cammino)

        print(self.peso_ottimo)
        print(self.percorso_ottimo)

    def ricorsione(self, percorso_parziale, nodo_finale, peso_parziale, lunghezza_cammino):


        if len(percorso_parziale) == lunghezza_cammino:
            if percorso_parziale[-1] == nodo_finale and peso_parziale > self.peso_ottimo:
                self.percorso_ottimo = copy.deepcopy(percorso_parziale)
                self.peso_ottimo = peso_parziale
                return

        else:
            for vicino in self.g.successors(percorso_parziale[-1]):
                if vicino not in percorso_parziale:
                    if self.g.has_edge(percorso_parziale[-1], vicino):
                        peso_nuovo = self.g[percorso_parziale[-1]][vicino]["weight"]
                        percorso_parziale.append(vicino)
                        if len(percorso_parziale) <= lunghezza_cammino:
                            self.ricorsione(percorso_parziale, nodo_finale, peso_parziale + peso_nuovo, lunghezza_cammino)
                            percorso_parziale.pop()
                        #else:
                            #return
                #else:
                    #continue

