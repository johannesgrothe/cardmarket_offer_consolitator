import copy
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
        return self._find_lowest(reference_offers)

    def _find_lowest(self, reference_offers: OfferCollection) -> Optional[OfferCollection]:
        # print(str(reference_offers))
        # print(reference_offers.sum())

        if hash(reference_offers) in self.checked_offers:
            return None
        self.checked_offers.append(hash(reference_offers))

        lowest_offer = reference_offers

        for card, offers in self.all_offers.items():
            for offer in offers:
                if offer.seller in reference_offers.sellers:

                    check_offers = copy.copy(reference_offers)
                    check_offers.remove(card)
                    check_offers.add(offer)
                    if check_offers.sum() <= reference_offers.sum():
                        checked_offer = self._find_lowest(check_offers)
                        if checked_offer.sum() < lowest_offer.sum():
                            lowest_offer = checked_offer

        return lowest_offer