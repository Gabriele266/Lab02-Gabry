# Module with all the domain classes
import re

"""Check if a string is a single word with no numbers, spaces, symbols, accepting also unicode chars"""
def is_valid_input(s: str) -> bool:
    exp = re.compile(r'^[^\W\d_]+$')
    return exp.match(s) is not None

class Translation:
    _alien: str
    _italian: str

    @staticmethod
    def validate(alien: str, italian: str) -> bool:
        return is_valid_input(alien) and is_valid_input(italian)

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
    def import_from_strings(self, alien: str, italian: str):
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


    """Execute a function to every translation passing the translation as first argument"""
    def foreach_trans(self, function):
        for alien in self._translations:
            key = alien.lower()
            function(Translation(key, self._translations[key]))

    """Map the entire dictionary to something else into a list"""
    def map_dictionary(self, function):
        l = []

        for alien in self._translations:
            key = alien.lower()
            l.append(function(Translation(key, self._translations[key])))

        return l



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

    def __str__(self):
        return f"Dictionary with {len(self._translations)} translations"