class Card:
    _expansion: str
    _name: str

    def __init__(self, expansion: str, name: str):
        self._expansion = expansion
        self._name = name

    def __str__(self):
        return f"{self._expansion} // {self._name}"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.name == other.name and self.expansion == other.expansion

    def __ne__(self, other):
        return not self == other

    @property
    def expansion(self) -> str:
        return self._expansion

    @property
    def name(self) -> str:
        return self._name
