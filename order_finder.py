import logging
import threading
from typing import Optional

from card import Card
from offer import Offer
from offer_collection import OfferCollection


class OrderFinder:
    _logger: logging.Logger
    _lock: threading.Lock
    all_offers: dict[Card, list[Offer]]
    _all_cards: list[Card]
    _performed_checks: int
    _total_checks: int

    def __init__(self, all_offers: dict[Card, list[Offer]]):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._lock = threading.Lock()
        self.all_offers = self._remove_single_sellers(all_offers)
        self._all_cards = [x for x in self.all_offers.keys()]
        self._performed_checks = 0

        self._total_checks = 1
        for _, offers in self.all_offers.items():
            self._total_checks *= len(offers)

    @property
    def total_checks(self) -> int:
        return self._total_checks

    def get_performed_checks(self) -> int:
        with self._lock:
            return self._performed_checks

    def _increment_check(self):
        with self._lock:
            self._performed_checks += 1

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
        return self._find_lowest(reference_offers, 0)

    def _find_lowest(self, reference_offers: OfferCollection, card_id: int) -> Optional[OfferCollection]:
        lowest_offer = reference_offers
        card = self._all_cards[card_id]
        buf_offer = lowest_offer.remove(card)

        for offer in self.all_offers[card]:
            if card_id < len(self.all_offers) - 1:
                checked_offer = self._find_lowest(buf_offer.add(offer), card_id + 1)  # TODO: add multithreading
            else:
                checked_offer = buf_offer.add(offer)
                self._increment_check()

            if checked_offer.sum() < lowest_offer.sum():
                lowest_offer = checked_offer
        return lowest_offer
