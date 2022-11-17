from copy import copy

from card import Card
from offer_set import OfferSet
from seller import Seller


class OfferCollection:
    offer_sets: list[OfferSet]
    _sum: float

    def __init__(self, offers: list[OfferSet]):
        self.offer_sets = offers
        self.offer_sets.sort()
        self._sum = round(sum([x.price for x in self.offer_sets]) + sum(x.shipping for x in self.sellers), 2)

    def __str__(self):
        return str([str(x) for x in self.offer_sets]) + f" for a total of {self.sum()}€"

    def __eq__(self, other):
        if not isinstance(other, OfferCollection):
            raise NotImplementedError()
        if not len(self.offer_sets) == len(other.offer_sets):
            return False
        for offer in self.offer_sets:
            if offer not in other.offer_sets:
                return False
        return True

    def __hash__(self):
        return hash(str([str(x) for x in self.offer_sets]))

    @property
    def sellers(self) -> list[Seller]:
        sellers = []
        for offer_set in self.offer_sets:
            for seller in offer_set.sellers:
                if seller not in sellers:
                    sellers.append(seller)
        return sellers

    def sum(self) -> float:
        return self._sum

    def add(self, offer: OfferSet):
        new_offers = copy(self.offer_sets)
        new_offers.append(offer)
        new_collection = OfferCollection(new_offers)
        return new_collection

    def remove(self, card: Card):
        new_offers = copy(self.offer_sets)
        for offer in new_offers:
            if offer.card == card:
                new_offers.remove(offer)

        new_collection = OfferCollection(new_offers)
        return new_collection
