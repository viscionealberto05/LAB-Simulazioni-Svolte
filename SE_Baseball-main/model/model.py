import copy

from database.dao import DAO
import networkx as nx
from operator import itemgetter

class Model:
    def __init__(self):
        self.lista_anni = []
        self.lista_squadre = []
        self.dizionario_squadre = {}
        self.dizionario_salari = {}
        self.g = nx.Graph()

    def get_years(self):
        self.lista_anni = DAO.get_years()

    def get_squadre(self, year):
        self.anno = int(year)
        self.lista_squadre = DAO.get_squadre(year)

        for squadra in self.lista_squadre:
            self.dizionario_squadre[squadra.id] = squadra

    def build_grafo(self):
        self.g.clear()
        self.g.add_nodes_from(self.lista_squadre)

        lista_salari = DAO.get_salari(self.anno) #lista di liste [[id_team, salario],[],[]]
        for squadra in lista_salari:
            self.dizionario_salari[int(squadra[0])] = squadra[1]

        for node_1 in self.g.nodes():
            for node_2 in self.g.nodes():
                if node_1 != node_2:
                    if self.g.has_edge(node_1, node_2):
                        pass
                    else:
                        peso = self.dizionario_salari[int(node_1.id)] + self.dizionario_salari[int(node_2.id)]
                        self.g.add_edge(node_1, node_2, weight=peso)

    def get_dettagli_squadra(self, id_sq):
        squadra = self.dizionario_squadre[int(id_sq)]

        lista_pesi_vicini = []

        for vicino in self.g.neighbors(squadra):
            dizionario = {"vicino":None,"peso":0.0}
            dizionario["vicino"] = vicino
            dizionario["peso"] = self.g[squadra][vicino]["weight"]
            lista_pesi_vicini.append(dizionario)

        self.lista_ordinata = sorted(lista_pesi_vicini, key=itemgetter('peso'), reverse=True)

        return self.lista_ordinata


    """def get_percorso_massimo(self, id_sq):
        squadra = self.dizionario_squadre[int(id_sq)]

        self.percorso_ottimo = []
        self.peso_ottimo = 0.0

        self.k = 3

        parziale = [squadra]
        self.ricorsione(parziale, 0, float("inf"))

        print(self.percorso_ottimo)

    def ricorsione(self, parziale, peso_tot, peso_ultimo_arco):
        if peso_tot >= self.peso_ottimo:
            self.percorso_ottimo = copy.deepcopy(parziale)
            self.peso_ottimo = peso_tot

        ultimo_nodo = parziale[-1]

        counter = 0
        lista_vicini_per_peso = self.get_dettagli_squadra(ultimo_nodo.id)

        for vicino in lista_vicini_per_peso:    #itero in ordine sui nodi con archi più pesanti sfruttando la funzione precedente
            counter += 1

            if vicino['vicino'] not in parziale:    #se il nodo non è tra quelli visitati
                    peso_arco = self.g[ultimo_nodo][vicino['vicino']]["weight"]
                    if peso_arco < peso_ultimo_arco: #condizione di decrescenza
                        parziale.append(vicino['vicino'])
                        self.ricorsione(parziale, peso_tot + peso_arco, peso_arco)
                        parziale.pop()
                    continue
            else:
                    continue"""

    def get_percorso_massimo(self, id_sq):
        squadra = self.dizionario_squadre[int(id_sq)]

        self.percorso_ottimo = []
        self.peso_ottimo = 0.0
        self.k = 3

        parziale = [squadra]
        self.ricorsione(parziale, 0, float("inf"))

        #print(self.percorso_ottimo, self.peso_ottimo)

    def ricorsione(self, parziale, peso_tot, peso_ultimo_arco):
        # aggiorna soluzione migliore
        if peso_tot > self.peso_ottimo:
            self.percorso_ottimo = parziale.copy()
            self.peso_ottimo = peso_tot

        ultimo_nodo = parziale[-1]

        counter = 0
        lista_vicini_per_peso = self.get_dettagli_squadra(ultimo_nodo.id)
        # lista_vicini_per_peso è già ordinata per peso decrescente

        for vicino in lista_vicini_per_peso:
            nodo_vicino = vicino['vicino']

            if nodo_vicino in parziale:
                continue

            peso_arco = self.g[ultimo_nodo][nodo_vicino]["weight"]

            # condizione di decrescenza
            if peso_arco <= peso_ultimo_arco:
                parziale.append(nodo_vicino)
                self.ricorsione(parziale, peso_tot + peso_arco, peso_arco)
                parziale.pop()

                counter += 1
                if counter == self.k:
                    break


