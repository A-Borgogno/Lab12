import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        years = self._model.getAllYears()
        for year in years:
            self._view.ddyear.options.append(ft.dropdown.Option(year))
        nations = self._model.getAllNations()
        for nation in nations:
            self._view.ddcountry.options.append(ft.dropdown.Option(nation))
        self._view.update_page()


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        self._view.btn_volume.disabled = False
        self._view.btn_path.disabled = False
        country = self._view.ddcountry.value
        year = self._view.ddyear.value
        graph = self._model.buildGraph(country, year)
        self._view.txt_result.controls.append(ft.Text(f"N nodi: {graph.number_of_nodes()} N archi: {graph.number_of_edges()}"))
        self._view.update_page()



    def handle_volume(self, e):
        archiIncidenti = self._model.getArchiIncidenti()
        for n in archiIncidenti.keys():
            self._view.txtOut2.controls.append(ft.Text(f"{n} --> {archiIncidenti[n]}"))
        self._view.update_page()

    def handle_path(self, e):
        pass
