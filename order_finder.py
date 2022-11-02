import copy
import sys
from typing import Optional

from card import Card
from offer import Offer
from offer_collection import OfferCollection


class OrderFinder:
    all_offers: dict[Card, list[Offer]]

    checked_offers: list[int]

    def __init__(self, all_offers: dict[Card, list[Offer]]):
        self.all_offers = all_offers
        self.checked_offers = []

    def find_lowest_offer(self) -> OfferCollection:
        reference_offers = OfferCollection([y[0] for x, y in self.all_offers.items()])
        sys.setrecursionlimit(7500)
        return self._find_lowest(reference_offers)

    def _find_lowest(self, reference_offers: OfferCollection) -> Optional[OfferCollection]:
        offer_hash = hash(reference_offers)
        if offer_hash in self.checked_offers:
            return None
        self.checked_offers.append(offer_hash)

        lowest_offer = copy.copy(reference_offers)

        for card, offers in self.all_offers.items():
            buf_offer = reference_offers.remove(card)
            for offer in offers:
                checked_offer = self._find_lowest(buf_offer.add(offer))
                if not checked_offer:
                    continue
                if checked_offer.sum() < lowest_offer.sum():
                    lowest_offer = checked_offer
        return lowest_offer
