import logging
import threading

from card import Card
from offer import Offer
from offer_collection import OfferCollection
from offer_set import OfferSet


class OrderFinder:
    _logger: logging.Logger
    _lock: threading.Lock
    # all_offers: dict[Card, list[OfferSet]]
    _offer_sets: list[list[OfferSet]]
    _all_cards: list[Card]
    _performed_checks: int
    _total_checks: int

    _lock: threading.Lock
    _returned_offer_collections: list[OfferCollection]

    def __init__(self, all_offers: dict[Card, list[Offer]]):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._lock = threading.Lock()
        buf_offers = self._remove_single_sellers(all_offers)
        all_offers = self._transform_to_sets(buf_offers)
        self._all_cards = [x for x in all_offers.keys()]
        self._performed_checks = 0

        self._total_checks = 1
        for _, offer_sets in all_offers.items():
            self._total_checks *= len(offer_sets)
        self._logger.info(f"Created OrderFinder for {len(all_offers)} cards")

        self._offer_sets = [y for x, y in all_offers.items()]
        self._offer_sets.sort(key=len)
        self._offer_sets.reverse()

        self._lock = threading.Lock()
        self._lowest_offer = OfferCollection([x[0] for x in self._offer_sets])

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
            if cheapest_offer not in new_offers:
                new_offers.append(cheapest_offer)
            self._logger.info(f"Reduced offer-count for '{card.name}' from {len(offers)} to {len(new_offers)}")
            out_data[card] = new_offers

        return out_data

    def _create_set(self, elem: OfferSet, offers: list[Offer]) -> list[OfferSet]:
        if elem.cards_available >= elem.card.amount:
            return [elem]
        buf_data = []
        for offer in offers:
            if offer not in elem.offers:
                buf_data += self._create_set(OfferSet(elem.offers + [offer]), offers)
        return buf_data

    def _create_sets(self, offers: list[Offer]) -> list[OfferSet]:
        buf_data = []

        for offer in offers:
            buf_data += self._create_set(OfferSet([offer]), offers)

        out_data = []
        for x in buf_data:
            if x not in out_data:
                out_data.append(x)
        return out_data

    def _transform_to_sets(self, in_data: dict[Card, list[Offer]]) -> dict[Card, list[OfferSet]]:
        out_data: dict[Card, list[OfferSet]] = {}
        for card, offers in in_data.items():
            out_data[card] = self._create_sets(offers)
            self._logger.info(f"Created {len(out_data[card])} offer-sets for '{card.name}'")
        return out_data

    def find_lowest_offer(self) -> OfferCollection:
        self._logger.info(f"Searching for lowest combination in {self.total_checks} total combinations")

        threads = []
        card = self._all_cards[0]
        buf_offer = self._lowest_offer.remove(card)
        for i, offer_set in enumerate(self._offer_sets[0]):
            thread = threading.Thread(target=self._find_lowest,
                                      args=[buf_offer.add(offer_set), 1],
                                      name=f"Thread_{i}",
                                      daemon=True)
            threads.append(thread)
            thread.start()

        with self._lock:
            return self._lowest_offer

    def _find_lowest(self, reference_offers: OfferCollection, card_id: int) -> None:
        card = self._all_cards[card_id]
        buf_offer = reference_offers.remove(card)

        for offer in self._offer_sets[card_id]:
            checked_offer = buf_offer.add(offer)
            if card_id < len(self._offer_sets) - 1:
                self._find_lowest(checked_offer, card_id + 1)
            else:
                self._increment_check()
                with self._lock:
                    if checked_offer.sum() < self._lowest_offer.sum():
                        self._lowest_offer = checked_offer
