import src.domain.classes as domain

def set_to_str(st: set[str]) -> str:
    list_equiv = list(st)
    s = list_equiv[0]

    if len(list_equiv) > 1:
        for t in range(1, len(list_equiv)):
            s += f",{list_equiv[t]}"

    return s

class TranslatorWorker:
    _filename: str

    def __init__(self, filename: str):
        self._filename = filename

    """Load unicode file with translations"""
    def load(self) -> domain.Dictionary:
        f = open(self._filename, "r", encoding="utf-8")
        dic = domain.Dictionary()

        for line in f.readlines():
            tk = line.split(" ")

            if len(tk) == 2:
                dic.import_from_strings(tk[0].strip(), tk[1].strip())

        f.close()
        return dic

    """Write the dictionary to a file"""
    def write(self, dc: domain.Dictionary):
        f = open(self._filename, "w", encoding="utf-8")

        dc.foreach_trans(lambda t: f.write(f"{t.alien} {set_to_str(t.italian)}\n"))
        f.close()