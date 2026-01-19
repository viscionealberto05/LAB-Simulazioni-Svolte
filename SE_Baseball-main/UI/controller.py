import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def popola_dd_anno(self):

        self._view.dd_anno.options.clear()

        self._model.get_years()

        for year in self._model.lista_anni:
            self._view.dd_anno.options.append(ft.DropdownOption(year))

    def year_setter(self,e):
        self.anno = int(e.control.value)
        self.popola_dd_squadre()

    def popola_dd_squadre(self):

        self._model.get_squadre(int(self.anno))

        self._view.dd_squadra.options.clear()

        for squadra in self._model.lista_squadre:
            self._view.dd_squadra.options.append(ft.DropdownOption(key=squadra.id, text=squadra.team_code))

        self._view.txt_out_squadre.controls.clear()

        self._view.txt_out_squadre.controls.append(ft.Text(f"Numero squadre: {len(self._model.lista_squadre)}"))

        for squadra in self._model.lista_squadre:
            self._view.txt_out_squadre.controls.append(ft.Text(f"{squadra.team_code} - {squadra.name}"))

        self._view.page.update()


    def team_setter(self,e):
        self.id_team_scelto = int(e.control.value)
        #print("team_scelto")

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        self._model.build_grafo()

    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        self._model.get_dettagli_squadra(self.id_team_scelto)

        self._view.txt_risultato.controls.clear()

        for dict in self._model.lista_ordinata:
            self._view.txt_risultato.controls.append(ft.Text(f"{dict['vicino'].name} - ({dict['vicino'].team_code}), peso:{dict['peso']}"))

        self._view.page.update()


    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        self._view.txt_risultato.controls.clear()

        self._model.get_percorso_massimo(self.id_team_scelto)

        for i in range(1,len(self._model.percorso_ottimo)):
            self._view.txt_risultato.controls.append(ft.Text(f"{self._model.percorso_ottimo[i-1]} - {self._model.percorso_ottimo[i]}, peso:{self._model.g[self._model.percorso_ottimo[i-1]][self._model.percorso_ottimo[i]]['weight']}"))

        self._view.page.update()


    """ Altri possibili metodi per gestire di dd_anno """""
    # TODO