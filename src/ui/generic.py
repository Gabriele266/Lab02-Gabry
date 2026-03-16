import flet as ft
from abc import *

class PageClass(ABC):
    """Represents an abstract page class helper"""
    def __init__(self):
        pass

    @abstractmethod
    def present(self, page: ft.Page):
        raise NotImplementedError("Implement in a subclass")