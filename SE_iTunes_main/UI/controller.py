import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def durata_setter(self,e):
        try:
            self.durata = int(e.control.value)
        except ValueError:
            self._view.alert.show_alert("Inserisci un valore valido.")

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        self._model.build_grafo(self.durata)

        self._view.dd_album.options.clear()

        self._view.lista_visualizzazione_1.controls.clear()

        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Grafo con {self._model.g.number_of_nodes()} nodi e {self._model.g.number_of_edges()} archi"))

        for nodo in self._model.g.nodes():
            self._view.dd_album.options.append(ft.DropdownOption(key=nodo.id ,text=nodo.title))

        self._view.page.update()

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        self.id_album_selezionato = int(e.control.value)

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        self._model.get_comp_connessa(self.id_album_selezionato)

        self._view.lista_visualizzazione_2.controls.clear()

        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Dim. comp connessa: {self._model.dim_comp_connessa}, durata totale {self._model.durata_tot} minuti."))

        self._view.page.update()

    def setter_durata_totale(self, e):
        try:
            self.durata_tot = e.control.value
        except ValueError:
            self._view.alert.show_alert("Inserisci un valore valido.")

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        self._model.compute_best_set(self.id_album_selezionato, self.durata_tot)
