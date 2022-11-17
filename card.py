from typing import Union


class Card:
    _expansions: list[str]
    _name: str
    _amount: int

    def __init__(self, expansions: Union[list[str], str], name: str, amount: int = 1):
        if isinstance(expansions, str):
            expansions = [expansions]
        self._expansions = expansions
        self._expansions.sort()
        self._name = name
        self._amount = amount

    def __str__(self):
        return f"{', '.join(self._expansions)} // {self._name} x {self.amount}"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.name == other.name and self.expansions == other.expansions

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(str(self))

    @property
    def expansions(self) -> list[str]:
        return self._expansions

    @property
    def name(self) -> str:
        return self._name

    @property
    def amount(self) -> int:
        return self._amount
