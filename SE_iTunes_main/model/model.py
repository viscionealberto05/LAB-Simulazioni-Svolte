import copy

import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.lista_album = []
        self.g = nx.Graph()

        self.dizionario_durate = {}
        self.mappa_album ={}

    def get_album(self, durata):
        self.lista_album = DAO.get_album(int(durata))

        for album in self.lista_album:
            self.mappa_album[int(album.id)] = album

    def load_durate(self, durata):
        lista_durate_album = DAO.get_durate(durata)
        for tupla in lista_durate_album:
            self.dizionario_durate[int(tupla[0])] = float(tupla[1])

    def build_grafo(self, durata):

        self.dizionario_durate = {}
        self.mappa_album = {}
        self.g.clear()

        self.get_album(durata)

        self.load_durate(durata)

        self.g.add_nodes_from(self.lista_album)

        "Aggiunta degli archi"

        lista_archi = DAO.get_edges() #lista di tuple, ciascuna tupla un arco

        lista_album_validi = []
        for key in self.dizionario_durate:
            lista_album_validi.append(key)

        for tupla in lista_archi:
            if tupla[0] in lista_album_validi and tupla[1] in lista_album_validi:
                self.g.add_edge(self.mappa_album[int(tupla[0])], self.mappa_album[int(tupla[1])])

        print(self.g)

    def get_comp_connessa(self, id_album):

        album = self.mappa_album[id_album]

        self.cc = nx.node_connected_component(self.g, album)

        self.dim_comp_connessa = len(self.cc)

        self.durata_tot = 0.0
        for nodo in self.cc:
            self.durata_tot += self.dizionario_durate[nodo.id]

    def compute_best_set(self, id_album, max_duration):
        """Ricerca ricorsiva del set massimo di album nella componente connessa"""
        start_album = self.mappa_album[id_album]
        component = self.get_component(start_album)
        self.soluzione_best = []
        self._ricorsione(component, [start_album], start_album.duration, max_duration)
        print(self.soluzione_best)
        return self.soluzione_best

    def _ricorsione(self, albums, current_set, current_duration, max_duration):
        if len(current_set) > len(self.soluzione_best):
            self.soluzione_best = current_set[:]

        for album in albums:
            if album in current_set:
                continue
            new_duration = current_duration + album.duration
            if new_duration <= max_duration:
                current_set.append(album)
                self._ricorsione(albums, current_set, new_duration, max_duration)
                current_set.pop()

    def get_component(self, album):
        """Restituisce la componente connessa di un album"""
        if album not in self.g:
            return []
        return list(nx.node_connected_component(self.g, album))











    """def get_set_album(self, durata_tot, id_album_partenza):
        self.durata_tot = float(durata_tot)
        self.album_partenza = self.mappa_album[id_album_partenza]

        self.lista_ottima = []

        lista_parziale = [self.album_partenza]
        lista_visitati = [self.album_partenza]



        self.ricorsione(lista_parziale, lista_visitati)

        print(self.lista_ottima)

    def ricorsione(self, lista_parziale, lista_visitati):

        if len(lista_visitati) == len(self.cc):

            #check durate
            durata_candidata = 0.0
            for nodo in lista_parziale:
                durata_candidata += self.dizionario_durate[nodo.id]

            if durata_candidata < self.durata_tot and len(lista_parziale) >= len(self.lista_ottima):
                self.lista_ottima = copy.deepcopy(lista_parziale)

        else:
            for nodo in self.cc:
                if nodo not in lista_visitati:
                    lista_parziale.append(nodo)
                    lista_visitati.append(nodo)
                    self.ricorsione(lista_parziale, lista_visitati)
                    lista_parziale.pop()
                    lista_visitati.pop()"""



