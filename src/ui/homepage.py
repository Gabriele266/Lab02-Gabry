import flet as ft
from src.ui.generic import PageClass
from src.domain.classes import Dictionary

class Homepage (PageClass):
    def __init__(self, dictionary: Dictionary):
        self._dictionary = dictionary
        super().__init__()

    def present(self, page: ft.Page):
        page.title = "Hello word application"

        page.add(
            ft.Text(f"Loaded {self._dictionary.size()}"),
        )