class Offer:
    _seller: str
    _amount: int
    _price: float

    def __init__(self, seller: str, amount: int, price: float):
        self._seller = seller
        self._amount = amount
        self._price = price

    def __str__(self):
        return f"{self._seller}: {self._amount} for {self._price}"

    @property
    def seller(self) -> str:
        return self._seller

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def price(self) -> float:
        return self._price
