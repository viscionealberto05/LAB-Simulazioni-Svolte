from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.mappa_hub = {}
        self.G = nx.Graph()

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
        guadagno medio per spedizione >= threshold (euro)
        """

        self.G.clear()

        self._nodes = DAO.get_hub()

        for nodo in self._nodes:
            self.mappa_hub[nodo.id] = nodo

        self._edges = DAO.get_tratta() #archi di tutti i tipi (1,2) e (2,1), duplicati presenti

        self.G.add_nodes_from(self._nodes)

        for tratta in self._edges:
            hub1 = self.mappa_hub[tratta.id_hub_1]
            hub2 = self.mappa_hub[tratta.id_hub_2]
            if self.G.has_edge(hub1,hub2):
                nuova_media = self.ricalcola_media(tratta)
                if nuova_media >= threshold:
                    self.G[hub1][hub2]["weight"] = nuova_media
            else:
                valore_tratta = (tratta.somma_tratta/tratta.n_spedizioni)
                if valore_tratta >= threshold:
                    self.G.add_edge(hub1,hub2,weight=valore_tratta)

        print(self.G)

    def ricalcola_media(self, tratta_nota):

        for tratta in self._edges:
            somma_tot = 0.0
            n_sped_tot = 0
            flag = False
            if tratta_nota.id_hub_1 == tratta.id_hub_1 and tratta_nota.id_hub_2 == tratta.id_hub_2:
                somma_tot += (tratta.somma_tratta)
                n_sped_tot += (tratta.n_spedizioni)
                #flag = True
            if tratta_nota.id_hub_2 == tratta.id_hub_1 and tratta_nota.id_hub_1 == tratta.id_hub_2:
                somma_tot += (tratta.somma_tratta)
                n_sped_tot += (tratta.n_spedizioni)
                #if flag == True:
                break
        return (somma_tot / n_sped_tot)

    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """
        # TODO

    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """
        # TODO

    def get_all_edges(self):
        """
        Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        # TODO

