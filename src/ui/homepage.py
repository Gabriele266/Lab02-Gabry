import flet as ft
from src.ui.generic import PageClass
from src.domain.classes import Dictionary
from src.ui.settings import GeneralSettings


class Homepage (PageClass):
    def __init__(self, dictionary: Dictionary):
        self._dictionary = dictionary
        super().__init__()

    def present(self, page: ft.Page):
        page.title = "Dictionary application - Gabry"

        page.add(
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Dictionary application", size=30, color=ft.Colors.WHITE),
                    ft.Text(f"Loaded dictionary from file {GeneralSettings.__FILENAME__} with {self._dictionary.size()} translations", size=12, color=ft.Colors.GREY),
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
