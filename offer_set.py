from offer import Offer


class OfferSet:
    _offers: list[Offer]
    _price: float

    def __init__(self, offers: list[Offer]):
        card = None
        for offer in offers:
            if card is None:
                card = offer.card
                continue
            if offer.card != card:
                raise ValueError(card)
        self._offers = offers
        self.offers.sort()
        self._price = self._calc_price()

    def __str__(self):
        return f"{len(self._offers)} offers for {self.card}"

    def __lt__(self, other):
        if not isinstance(other, OfferSet):  # TODO: would also work with Offer
            raise NotImplementedError()
        return self.price < other.price

    def _calc_price(self) -> float:
        buf_sum = 0
        added_cards = 0
        for offer in self._offers:
            for i in range(offer.amount):
                if added_cards > self.card.amount:
                    break
                added_cards += 1
                buf_sum += offer.price
        return buf_sum

    @property
    def price(self) -> float:
        """
        :return: Cheapest price to n cards without shipping
        """
        return self._price

    @property
    def offers(self) -> list[Offer]:
        return self._offers

    @property
    def card(self):
        return self._offers[0].card

    @property
    def sellers(self):
        return [x.seller for x in self._offers]
