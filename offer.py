from card import Card
from seller import Seller


class Offer:
    _card: Card
    _seller: Seller
    _amount: int
    _price: float
    _expansion: str

    def __init__(self, card: Card, seller: Seller, amount: int, price: float, expansion: str):
        self._card = card
        self._seller = seller
        self._amount = amount
        self._price = price
        self._shipping = 1.15
        self._expansion = expansion

    def __str__(self):
        # return f"{self._seller}: {self._amount} for {self._price}"
        return f"{self._card}: {self._amount} for {self._price} by {self._seller}"

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        if not isinstance(other, Offer):
            raise NotImplementedError()
        return self.price < other.price

    def __eq__(self, other):
        if not isinstance(other, Offer):
            raise NotImplementedError()
        return (self.price == other.price and
                self.card == other.card and
                self.amount == other.amount and
                self.seller == other.seller)

    @property
    def card(self) -> Card:
        return self._card

    @property
    def seller(self) -> Seller:
        return self._seller

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def price(self) -> float:
        return self._price

    @property
    def expansion(self) -> str:
        return self._expansion
