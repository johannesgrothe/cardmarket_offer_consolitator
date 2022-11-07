from offer import Offer


class OfferSet:
    _offers: list[Offer]
    _price: float
    _distribution: dict[Offer, int]

    def __init__(self, offers: list[Offer]):
        checked = []
        for offer in offers:
            if offer in checked:
                raise ValueError(f"Double Element '{offer}' detected")
            checked.append(offer)

        card = None
        for offer in offers:
            if card is None:
                card = offer.card
                continue
            if offer.card != card:
                raise ValueError(f"Card '{card}' does not match other cards ({card})")
        self._offers = offers
        self.offers.sort()
        self._distribution = self._calc_distribution()
        self._price = sum([offer.price * amount for offer, amount in self._distribution.items()])

    def __str__(self):
        return f"{len(self._offers)} offers for {self.card}"

    def __eq__(self, other):
        if not isinstance(other, OfferSet):
            raise NotImplementedError()
        return self.offers == other.offers

    def __lt__(self, other):
        if not isinstance(other, OfferSet):  # TODO: would also work with Offer
            raise NotImplementedError()
        return self.price < other.price

    def _calc_distribution(self) -> dict[Offer, int]:
        dist = {}
        added_cards = 0
        for offer in self._offers:
            local_amount = 0
            for i in range(offer.amount):
                if added_cards > self.card.amount:
                    break
                local_amount += 1
                added_cards += 1
            dist[offer] = local_amount
        return dist

    def get_amount_for_offer(self, offer: Offer) -> int:
        return self._distribution[offer]

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

    @property
    def cards_available(self) -> int:
        return sum([x.amount for x in self._offers])
