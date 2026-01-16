import copy

import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self.lista_rifugi = []
        self.mappa_rifugi = {}

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """

        self.G.clear()

        self.lista_rifugi = DAO.get_rifugi()
        self.lista_connessioni = DAO.get_connessioni(int(year))

        for rifugio in self.lista_rifugi:
            self.mappa_rifugi[rifugio.id] = rifugio

        lista_archi = []
        self.lista_archi_pesati = []

        for connessione in self.lista_connessioni:
            if (connessione.id_rifugio1, connessione.id_rifugio2)  and  (connessione.id_rifugio2, connessione.id_rifugio1) not in lista_archi:
                coeff_difficolta = self.get_diff(connessione.difficolta)
                peso = float(connessione.distanza) * float(coeff_difficolta)
                lista_archi.append((connessione.id_rifugio1, connessione.id_rifugio2))
                self.lista_archi_pesati.append([connessione.id_rifugio1, connessione.id_rifugio2,peso])

        for arco in self.lista_archi_pesati:
            self.G.add_edge(self.mappa_rifugi[arco[0]], self.mappa_rifugi[arco[1]], weight=arco[2])

        print(self.G)


    def get_diff(self, difficolta):
        if difficolta == "facile":
            return 1
        if difficolta == "media":
            return 1.5
        if difficolta == "difficile":
            return 2


    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """

        max = 0.0
        min = float("inf")
        for arco in self.lista_archi_pesati:
            if arco[2] > max:
                max = arco[2]
            if arco[2] < min:
                min = arco[2]

        return min, max


    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """

        self.soglia = soglia

        somma_sopra = 0
        somma_sotto = 0
        for arco in self.lista_archi_pesati:
            if arco[2] > soglia:
                somma_sopra += 1
            if arco[2] < soglia:
                somma_sotto += 1

        return somma_sotto, somma_sopra

    def shortest_path_recursive(self, soglia):
        """
        Restituisce la lista di nodi del cammino minimo (somma dei pesi minima) il cui percorso è fatto solo da archi
        con peso >soglia (usa la ricorsione). Se non esiste alcun percorso valido restituisce [].
        :param soglia: il cammino minimo individuato deve essere fatto da archi il cui peso deve essere >soglia
        :return: il cammino minimo come lista di archi [(u,v,attr), ...] oppure []
        """
        # stato per la ricerca
        self.sol_best_edges = []  # lista di archi (u,v,attr) della migliore soluzione trovata
        self.best_cost = float('inf')  # costo minimo trovato

        # avvia ricerca da ogni nodo
        for n in self.G.nodes():
            partial = [n]
            partial_edges = []
            self._ricorsione(partial, partial_edges, soglia)

        print(self.sol_best_edges)
        return self.sol_best_edges

    def _ricorsione(self, partial_nodes, partial_edges, soglia):
        """
        Ricorsione che esplora percorsi semplici composti da archi con peso > soglia.
        :param partial_nodes: lista di nodi già considerati nel cammino
        :param partial_edges: lista di archi già considerati nel cammino
        :param soglia: la soglia oltre la quale deve essere il peso di ogni arco
        """
        # valuta SEMPRE il cammino corrente
        if partial_edges:
            cost = self._compute_weight_path(partial_edges)

            # pruning
            if cost >= self.best_cost:
                return

            # cammino valido come Dijkstra
            if len(partial_edges) >= 2:
                self.best_cost = cost
                self.sol_best_edges = partial_edges[:]

        n_last = partial_nodes[-1]
        neighs = self._get_admissible_neighbs(n_last, partial_nodes, soglia)

        for v in neighs:
            edge_attr = self.G.get_edge_data(n_last, v)
            partial_nodes.append(v)
            partial_edges.append((n_last, v, edge_attr))
            self._ricorsione(partial_nodes, partial_edges, soglia)
            partial_nodes.pop()
            partial_edges.pop()

    def _get_admissible_neighbs(self, node, partial_nodes, soglia):
        """
        Restituisce i vicini ammissibili:
          - non ancora visitati (evita cicli)
          - l'arco (node, v) esiste e ha 'weight' > soglia
        :param node: il nodo da considerare
        :param partial_nodes: lista di nodi già considerati nel cammino
        :param soglia: la soglia oltre la quale deve essere il peso di ogni arco
        :return: lista di vicini ammissibili
        """
        neighs = []
        for v in self.G.neighbors(node):
            if v in partial_nodes:
                continue
            attr = self.G.get_edge_data(node, v)
            if not attr:
                continue
            w = attr.get('weight', None)
            if w is None:
                continue
            # ora consideriamo solo archi con peso maggiore di soglia
            if w > soglia:
                neighs.append(v)
        return neighs

    def _compute_weight_path(self, edges):
        """
        Somma i pesi della lista 'edges' (elementi: (u,v,attr)).
        :param edges: lista di archi
        :return: la somma dei pesi di ogni arco
        """
        total = 0.0
        for _, _, attr in edges:
            if attr:
                total += float(attr.get('weight', 0.0))
        return total




    """Implementare la parte di ricerca del cammino minimo
    def handle_cammino_minimo(self):
        #print("cammino minimo")

        self.cammino_ottimo = []
        self.peso_ottimo = float("inf")

        for nodo in self.G.nodes():
            parziale = [nodo]
            peso_parziale = 0.0
            self.ricorsione(parziale, peso_parziale, self.soglia)

        for i in range(0,len(self.cammino_ottimo)):
            if i != len(self.cammino_ottimo)-1:
                print(f"{self.cammino_ottimo[i]} - {self.cammino_ottimo[i+1]}")

    def ricorsione(self, parziale, peso_parziale, soglia):
        if len(parziale) >2:
            if len(parziale) <= len(self.cammino_ottimo):
                self.cammino_ottimo = copy.deepcopy(parziale)
                self.peso_ottimo = peso_parziale
                return


        for neighbor in self.G.neighbors(parziale[-1]):
            if neighbor not in parziale:
                weight = self.G[parziale[-1]][neighbor]["weight"]
                if weight>soglia:
                    if peso_parziale+weight < self.peso_ottimo:
                        parziale.append(neighbor)
                        self.ricorsione(parziale, peso_parziale+weight,self.soglia)
                        parziale.pop()"""
