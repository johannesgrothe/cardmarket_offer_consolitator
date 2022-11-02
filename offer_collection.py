from copy import copy

from card import Card
from offer import Offer
from seller import Seller


class OfferCollection:
    offers: list[Offer]

    def __init__(self, offers: list[Offer]):
        self.offers = offers
        self.offers.sort()

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
            seller = offer.seller
            if seller not in sellers:
                sellers.append(seller)
        return sellers

    def sum(self) -> float:
        return sum([x.price for x in self.offers]) + sum(x.shipping for x in self.sellers)

    def add(self, offer: Offer):
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
