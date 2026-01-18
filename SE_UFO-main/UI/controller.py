import flet as ft
from model.model import Model
from UI.view import View

class Controller:
    def __init__(self, view : View, model : Model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        self._model.get_years()
        self._model.get_shapes()

        self._view.dd_year.options.clear()
        self._view.dd_shape.options.clear()

        for year in self._model.lista_anni:
            self._view.dd_year.options.append(ft.DropdownOption(year))

        for shape in self._model.lista_forme:
            self._view.dd_shape.options.append(ft.DropdownOption(shape))

    def year_setter(self,e):
        self.year = int(e.control.value)

    def shape_setter(self,e):
        self.shape = e.control.value

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """

        self._model.build_graph(self.year, self.shape)
        self._view.lista_visualizzazione_1.controls.clear()

        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Arco con {self._model.g.number_of_nodes()} nodi e {self._model.g.number_of_edges()} archi."))

        for res in self._model.lista_res:
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f"{res[0].id} - {res[1]}"))

        self._view.page.update()




    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        self._model.compute_path()

        self._view.lista_visualizzazione_2.controls.clear()

        # Mostra peso cammino massimo
        self._view.lista_visualizzazione_2.controls.append(
            ft.Text(f"Peso cammino massimo: {self._model.sol_best}")
        )

        # Mostra dettagli percorso
        for edge in self._model.path_edge:
            self._view.lista_visualizzazione_2.controls.append(
                ft.Text(
                    f"{edge[0].id} --> {edge[1].id}: "
                    f"peso {edge[2]} "
                    f"distanza {self._model.get_distance_weight(edge)}"
                )
            )

        self._view.update()