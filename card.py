class Card:
    _expansion: str
    _name: str
    _amount: int

    def __init__(self, expansion: str, name: str, amount: int = 1):
        self._expansion = expansion
        self._name = name
        self._amount = amount

    def __str__(self):
        return f"{self._expansion} // {self._name} x {self.amount}"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.name == other.name and self.expansion == other.expansion

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(str(self))

    @property
    def expansion(self) -> str:
        return self._expansion

    @property
    def name(self) -> str:
        return self._name

    @property
    def amount(self) -> int:
        return self._amount
