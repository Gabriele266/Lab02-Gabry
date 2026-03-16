import flet as ft
from src.ui.generic import PageClass
from src.domain.classes import Dictionary, Translation
from src.ui.settings import GeneralSettings


class Homepage (PageClass):
    def __init__(self, dictionary: Dictionary):
        self._dictionary = dictionary
        super().__init__()

    def present(self, page: ft.Page):
        page.title = "Dictionary application - Gabry"
        page.on_close = self.__on_close

        page.add(
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Dictionary application", size=30, color=ft.Colors.WHITE),
                    ft.Text(f"Loaded dictionary from file {GeneralSettings.__FILENAME__} with {self._dictionary.size()} translations", size=12, color=ft.Colors.GREY),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                           ft.Text("Search"),
                            ft.SearchBar(bar_hint_text="Search alien in dictionary...", bar_trailing=[ft.Icon(ft.Icons.SEARCH)], on_submit=self.__on_search_enter),
                        ]
                    ),
                    ft.Container(
                        border_radius=10,
                        border=ft.Border.all(2, ft.Colors.WHITE),
                        content=ft.Column(
                            height=600,
                            expand=True,
                            scroll=ft.ScrollMode.ALWAYS,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[ft.DataTable(
                                columns=[
                                    ft.DataColumn(
                                        label=ft.Text("Alien term")
                                    ),
                                    ft.DataColumn(
                                        label=ft.Text("Italian translations")
                                    ),
                                    ft.DataColumn(
                                        label=ft.Text("Actions")
                                    )
                                ],
                            rows=self._format_rows()
                    )]))
                ]
            )
        )

    def _format_rows(self) -> list[ft.DataRow]:
        rows = []

        self._dictionary.map_dictionary(lambda translation: rows.append(ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(translation.alien)),
                ft.DataCell(ft.Text(translation.translate())),
                ft.DataCell(ft.Row([ft.Button(icon=ft.Icons.EDIT, content="Edit"), ft.Button(icon=ft.Icons.DELETE, content="Delete")]))
            ]
        )))

        return rows

    def __on_search_enter(self, event: ft.Event[ft.SearchBar]):
        print(event)
        pass        # TODO: Implement search

    def __on_translation_delete(self, translation: Translation):
        pass        # TODO: Implement delete

    def __on_close(self, event: ft.Event[ft.Page]):
        quit()