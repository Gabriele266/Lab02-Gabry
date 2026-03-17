import re

class Wildcard:
    __wildcard__regex__ = r"^[^\W\d_]*+[?][^\W\d_]*+$"      # regex for wildcard validation

    def __init__(self, wildcard: str):
        self._wildcard: str = wildcard.lower()

        if not self.validate():
            raise ValueError(f"Invalid wildcard supplied {wildcard}")

    def validate(self) -> bool:
        """Check if a string is a wildcard or not."""
        return re.compile(self.__wildcard__regex__).match(self._wildcard) is not None

    def matches(self, string: str) -> bool:
        # convert the wildcard into a search regex
        tk = self._wildcard.split("?")
        if len(tk) != 2:        # in case the ? is at the end of the wildcard
            tk.append("")

        rx_str = f"^{tk[0]}[^\W\d_]{tk[1]}"

        # cia?milano
        match_regex = re.compile(rx_str)

        #   check if regex matches
        return match_regex.match(string) is not None