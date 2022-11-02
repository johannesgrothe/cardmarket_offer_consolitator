class Seller:
    _name: str
    _shipping: float

    def __init__(self, name: str, shipping: float):
        self._name = name
        self._shipping = shipping

    def __str__(self):
        return f"{self._name} ({self._shipping})"

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if not isinstance(other, Seller):
            raise NotImplementedError()
        return self.name == other.name and self.shipping == other.shipping

    @property
    def name(self) -> str:
        return self._name

    @property
    def shipping(self) -> float:
        return self._shipping
