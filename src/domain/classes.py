# Module with all the domain classes
from gettext import translation


class Translation:
    _alien: str
    _italian: str

    @staticmethod
    def validate(alien: str, italian: str) -> bool:
        return alien.isalpha() and italian.isalpha()

    """Create a new translation and control the values set"""
    def __init__(self, alien: str, italian: str):
        if not Translation.validate(alien, italian):
            raise ValueError("Invalid input")

        self._alien = alien.lower()
        self._italian = italian.lower()

    @property
    def alien(self) -> str:
        return self._alien

    @property
    def italian(self):
        return self._italian

    """Return true if this term has only one tranlsation"""
    def isunique(self) -> bool:
        # TODO: Implement multiple translations
        return True

    def __eq__(self, other):
        return self.alien == other.alien and self.italian == other.italian

class Dictionary:
    _translations: list[Translation] = {}        # dizionario con alien - italian

    def __init__(self):
        self._translations: dict[str, str] = {}

    """Append a new translation to the dictionary and verify the validity"""
    def add(self, alien: str, italian: str):
        t = Translation(alien, italian)
        self._translations[t.alien] = t.italian

    def add_translation(self, t: Translation):
        self._translations[t.alien] = t.italian

    """Returns the list of all the alien terms that have a translation"""
    def _get_translatable(self) -> list[str]:
        return list(self._translations.keys())

    def size(self) -> int:
        return len(self._translations.keys())

    def exists(self, alien: str) -> bool:
        return alien.lower() in self._get_translatable()

    def remove(self, alien: str):
        if not self.exists(alien):
            raise ValueError(f"The translation '{alien}' does not exist")

        self._translations.pop(alien.lower())

    """Get the translation for an alien term
    Note: returns the tranlsation object to handle multiple translations"""
    def get_translation(self, alien: str) -> Translation:
        return Translation(alien.lower(), self._translations[alien.lower()])

    @classmethod
    def from_translations(cls, translations: list[Translation]):
        dictionary = cls()
        for t in translations:
            dictionary.add_translation(t)

        return dictionary