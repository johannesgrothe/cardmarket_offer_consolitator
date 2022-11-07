from copy import copy

from card import Card
from offer import Offer
from offer_set import OfferSet
from seller import Seller


class OfferCollection:
    offers: list[OfferSet]
    _sum: float

    def __init__(self, offers: list[OfferSet]):
        self.offers = offers
        self.offers.sort()
        self._sum = round(sum([x.price for x in self.offers]) + sum(x.shipping for x in self.sellers), 3)

    def __str__(self):
        return str([str(x) for x in self.offers])

    def __eq__(self, other):
        if not isinstance(other, OfferCollection):
            raise NotImplementedError()
        if not len(self.offers) == len(other.offers):
            return False
        for offer in self.offers:
            if offer not in other.offers:
                return False
        return True

    def __hash__(self):
        return hash(str([str(x) for x in self.offers]))

    @property
    def sellers(self) -> list[Seller]:
        sellers = []
        for offer in self.offers:
            for seller in offer.sellers:
                if seller not in sellers:
                    sellers.append(seller)
        return sellers

    def sum(self) -> float:
        return self._sum

    def add(self, offer: OfferSet):
        new_offers = copy(self.offers)
        new_offers.append(offer)
        new_collection = OfferCollection(new_offers)
        return new_collection

    def remove(self, card: Card):
        new_offers = copy(self.offers)
        for offer in new_offers:
            if offer.card == card:
                new_offers.remove(offer)

        new_collection = OfferCollection(new_offers)
        return new_collection
