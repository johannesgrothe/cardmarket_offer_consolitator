import copy
import logging
import sys
from typing import Optional

from card import Card
from offer import Offer
from offer_collection import OfferCollection


class OrderFinder:
    _logger: logging.Logger
    all_offers: dict[Card, list[Offer]]
    checked_offers: list[int]

    def __init__(self, all_offers: dict[Card, list[Offer]]):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.all_offers = self._remove_single_sellers(all_offers)
        self.checked_offers = []

    def _remove_single_sellers(self, in_data: dict[Card, list[Offer]]) -> dict[Card, list[Offer]]:
        all_sellers = {}
        for card, offers in in_data.items():
            for offer in offers:
                if offer.seller in all_sellers:
                    all_sellers[offer.seller] += 1
                else:
                    all_sellers[offer.seller] = 1

        double_sellers = [x for x, y in all_sellers.items() if y > 1]
        out_data = {}

        for card, offers in in_data.items():
            offers.sort()
            new_offers = [x for x in offers if x.seller in double_sellers]
            cheapest_offer = offers[0]
            offers.sort()
            if cheapest_offer not in new_offers:
                new_offers.append(cheapest_offer)
            self._logger.info(f"Reduced offer-count for '{card.name}' from {len(offers)} to {len(new_offers)}")
            out_data[card] = new_offers

        return out_data

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
