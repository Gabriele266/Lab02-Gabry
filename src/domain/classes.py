# Module with all the domain classes
import re
from io import UnsupportedOperation

"""Check if a string is a single word with no numbers, spaces, symbols, accepting also unicode chars"""
def is_valid_input(s: str) -> bool:
    exp = re.compile(r'^[^\W\d_]+$')
    return exp.match(s) is not None

class Translation:
    _alien: str
    _italian: set[str]

    """Check if a new translation is valid (single italian term)"""
    @staticmethod
    def validate(alien: str, italian: str) -> bool:
        return is_valid_input(alien) and is_valid_input(italian)

    @staticmethod
    def from_multiple(alien: str, italians: list[str]):
        if not is_valid_input(alien):
            raise ValueError("Invalid alien term")

        if len(italians) == 0:
            raise ValueError("At least one italian term is required")

        if not is_valid_input(italians[0]):
            raise ValueError("Invalid translation")

        t = Translation(alien, italians[0])
        for i in range(1, len(italians)):
            if not is_valid_input(italians[i]):
                raise ValueError(f"Invalid input for italian {italians[i]}")
            t.append_alternative(italians[i])

        return t

    """Create a new translation and control the values set"""
    def __init__(self, alien: str, italian: str):
        if not Translation.validate(alien, italian):
            raise ValueError("Invalid input")

        self._alien = alien.lower()
        self._italian = {italian.lower()}

    @property
    def alien(self) -> str:
        return self._alien

    @property
    def italian(self) -> set[str]:
        return self._italian

    """Returns the first translation available. Attention if the translation is not unique --> The order is not respected"""
    def translate(self) -> str:
        return list(self._italian)[0]

    """Add a new translation for the same term"""
    def append_alternative(self, alternative: str):
        self._italian.add(alternative)

    """Return true if this term has only one tranlsation"""
    def isunique(self) -> bool:
        return len(self._italian) == 1

    def __eq__(self, other):
        return self.alien == other.alien and self.italian == other.italian

class Dictionary:
    _translations: dict[str, set[str]] = {}        # dizionario con alien - italian

    def __init__(self):
        self._translations: dict[str, set[str]] = {}

    """Append a new translation to the dictionary and verify the validity"""
    def import_from_strings(self, alien: str, italian: str):
        t = Translation(alien, italian)
        self.add_translation(t)

    def add_translation(self, t: Translation):
        if self.exists(t.alien):        # if translation already exists, add the new term
            self._translations[t.alien].add(t.translate())
        else:
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

    """Count how many alien words have multiple translations """
    @property
    def multiple_translations(self) -> int:
        i = 0
        for t in self._translations:
            if len(self._translations[t]) > 1:
                i += 1
        return i

    """Count how many words have single translations """
    @property
    def single_translations(self) -> int:
        return self.size() - self.multiple_translations

    """Execute a function to every translation passing the translation as first argument"""
    def foreach_trans(self, function):
        for alien in self._translations:
            key = alien.lower()
            function(Translation.from_multiple(key, list(self._translations[key])))

    """Map the entire dictionary to something else into a list"""
    def map_dictionary(self, function):
        l = []

        for alien in self._translations:
            key = alien.lower()
            l.append(function(Translation.from_multiple(key, list(self._translations[key]))))

        return l



    """Get the translation for an alien term
    Note: returns the tranlsation object to handle multiple translations"""
    def get_translation(self, alien: str) -> Translation:
        return Translation.from_multiple(alien.lower(), list(self._translations[alien.lower()]))

    @classmethod
    def from_translations(cls, translations: list[Translation]):
        dictionary = cls()
        for t in translations:
            dictionary.add_translation(t)

        return dictionary

    def __str__(self):
        return f"Dictionary with {len(self._translations)} translations"