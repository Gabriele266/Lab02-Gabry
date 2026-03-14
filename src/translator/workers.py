import src.domain.classes as domain

class TranslatorLoader:
    _filename: str

    def __init__(self, filename: str):
        self._filename = filename

    """Load unicode file with translations"""
    def load(self) -> domain.Dictionary:
        f = open(self._filename, "r", encoding="utf-8")
        dic = domain.Dictionary()

        for line in f.readlines():
            tk = line.split(" ")
            dic.import_from_strings(tk[0].strip(), tk[1].strip())

        return dic