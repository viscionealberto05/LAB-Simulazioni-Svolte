from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def popola_dd_categorie(self):
        self._model.get_categories()

        for categoria in self._model.lista_categorie:
            self._view.dd_category.options.append(ft.DropdownOption(key=categoria.id, text=categoria.category_name))

    def categoria_setter(self,e):
        self.id_categoria_scelta = int(e.control.value)
        print(f"id_categoria_scelta: {self.id_categoria_scelta}")

    """def data_inizio_setter(self,e):
        self.data_inizio = e.control.value

    def data_fine_setter(self,e):
        self.data_fine = e.control.value"""

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        self._model.get_products(self.id_categoria_scelta)
        self._model.get_prodotti_venduti(self.id_categoria_scelta, self._view.dp1.value, self._view.dp2.value)
        self._model.build_graph()

        self._view.txt_risultato.controls.clear()

        n_nodi = self._model.g.number_of_nodes()
        n_archi = self._model.g.number_of_edges()
        self._view.txt_risultato.controls.append(ft.Text(f"Grafo con {n_nodi} nodi e {n_archi} archi"))

        self._view.dd_prodotto_iniziale.options.clear()
        self._view.dd_prodotto_finale.options.clear()

        for nodo in self._model.g.nodes():
            self._view.dd_prodotto_iniziale.options.append(ft.DropdownOption(key=nodo.id, text=nodo.product_name))
            self._view.dd_prodotto_finale.options.append(ft.DropdownOption(key=nodo.id, text=nodo.product_name))

        self._view.page.update()

    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        self._model.get_prodotti_migliori()

        for i in range(0,5):
            nome_prodotto = self._model.lista_ordinata[i]["prodotto"].product_name
            peso = self._model.lista_ordinata[i]["somma"]
            self._view.txt_risultato.controls.append(ft.Text(f"Prodotto: {nome_prodotto}, Peso: {peso}"))

        self._view.page.update()

    def id_prod_iniziale_setter(self,e):
        self.id_prod_iniziale = int(e.control.value)

    def id_prod_finale_setter(self,e):
        self.id_prod_finale = int(e.control.value)

    def lunghezza_cammino_setter(self,e):
        try:
            self.lunghezza_cammino = int(e.control.value)
            #eccezione anche se negativo
        except ValueError:
            self._view.alert.show_alert("Inserire un valore valido.")


    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        self._model.cerca_cammino(self.id_prod_iniziale, self.id_prod_finale, self.lunghezza_cammino)

        self._view.txt_risultato.controls.clear()

        self._view.txt_risultato.controls.append(ft.Text(f"Peso Cammino: {self._model.peso_ottimo}"))
        for nodo in self._model.percorso_ottimo:
            self._view.txt_risultato.controls.append(ft.Text(f"Prodotto: {nodo.product_name}"))

        self._view.page.update()

