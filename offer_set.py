import copy
import logging

from offer import Offer


class OfferSet:
    _price: float
    _distribution: dict[Offer, int]
    _logger: logging.Logger

    def __init__(self, offers: list[Offer]):
        self._logger = logging.getLogger(self.__class__.__name__)

        checked = []
        for offer in offers:
            if offer in checked:
                raise ValueError(f"Double Element '{offer}' detected")
            if offer.card != offers[0].card:
                raise ValueError("All offers must be for the same card")
            checked.append(offer)

        self._distribution = self._calc_distribution(offers)
        self._distribution = self._remove_unused_offers()
        self._price = sum([offer.price * amount for offer, amount in self._distribution.items()])

    def __str__(self):
        return f"{len(self._distribution)} offers for {self.card.name} by {', '.join([x.name for x in self.sellers])}"

    def __eq__(self, other):
        if not isinstance(other, OfferSet):
            raise NotImplementedError()
        return self.offers == other.offers

    def __lt__(self, other):
        if not isinstance(other, OfferSet):
            raise NotImplementedError()
        return self.price < other.price

    def _remove_unused_offers(self):
        out_distribution = {}
        for offer, amount in self._distribution.items():
            if amount != 0:
                out_distribution[offer] = amount
        return out_distribution

    @staticmethod
    def _calc_distribution(offers: list[Offer]) -> dict[Offer, int]:
        offers.sort(key=lambda x: (x.price, -x.amount))
        dist = {}
        added_cards = 0
        target_amount = offers[0].card.amount
        for offer in offers:
            local_amount = 0
            for i in range(offer.amount):
                if added_cards >= target_amount:
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
        return [x for x in self._distribution]

    @property
    def card(self):
        return self.offers[0].card

    @property
    def sellers(self):
        return [x.seller for x in self._distribution]

    @property
    def cards_available(self) -> int:
        return sum([x.amount for x in self._distribution])
