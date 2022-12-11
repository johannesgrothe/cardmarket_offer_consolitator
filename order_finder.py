import logging
import threading
from typing import Optional

from card import Card
from offer import Offer
from offer_collection import OfferCollection
from offer_set import OfferSet
from set_creator import OfferSetCreator


class OrderFinder:
    _logger: logging.Logger
    _lock: threading.Lock
    _offer_sets: list[list[OfferSet]]
    _all_cards: list[Card]
    _performed_checks: int
    _total_checks: int

    _total_threads: int
    _threads_started: int

    _lock: threading.Lock
    _returned_offer_collections: list[OfferCollection]

    def __init__(self, all_offers: dict[Card, list[Offer]]):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._lock = threading.Lock()
        buf_offers = all_offers
        # buf_offers = self._remove_single_sellers(all_offers)
        # buf_offers = self._remove_expensive_offers(buf_offers)
        buf_offers = self._transform_to_sets(buf_offers)
        self._all_cards = [x for x in buf_offers.keys()]
        self._performed_checks = 0

        self._offer_sets = [y for x, y in buf_offers.items()]
        self._offer_sets.sort(key=len)
        self._offer_sets.reverse()

        self._total_checks = 1
        for offer_sets in self._offer_sets:
            self._total_checks *= len(offer_sets)
        self._logger.info(f"Created OrderFinder for {len(buf_offers)} cards")

        self._lock = threading.Lock()
        reference_sets = [x[0] for x in self._offer_sets]
        self._lowest_offer = OfferCollection(reference_sets)

    @property
    def total_checks(self) -> int:
        return self._total_checks

    @property
    def performed_checks(self) -> int:
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
            new_offers = [x for x in offers if x.seller in double_sellers]
            new_offers.sort(key=lambda x: x.price)
            cheapest_offer = offers[0]
            if cheapest_offer not in new_offers:
                new_offers.append(cheapest_offer)
            self._logger.info(f"Reduced offer-count for '{card.name}' from {len(offers)} to {len(new_offers)}")
            out_data[card] = new_offers

        return out_data

    def _remove_expensive_offers(self, in_data: dict[Card, list[Offer]]) -> dict[Card, list[Offer]]:
        out_data = {}
        for card, offers in in_data.items():
            if card.amount > 1:
                out_data[card] = offers
                continue
            offers.sort(key=lambda x: x.price)
            base_price = offers[0].price + offers[0].seller.shipping
            new_offers = []
            for offer in offers:
                if offer.price <= base_price:
                    new_offers.append(offer)
            out_data[card] = new_offers
            self._logger.info(f"Reduced amount of offers for {card.name} from {len(offers)} to {len(new_offers)}")
        return out_data

    def _transform_to_sets(self, in_data: dict[Card, list[Offer]]) -> dict[Card, list[OfferSet]]:
        out_data: dict[Card, list[OfferSet]] = {}
        for card, offers in in_data.items():
            out_data[card] = OfferSetCreator(offers).sets
            self._logger.info(f"Created {len(out_data[card])} offer-sets for '{card.name}'")
        return out_data

    def find_lowest_offer(self, thread_count: int = 5) -> OfferCollection:
        self._logger.info(f"Searching for lowest combination in {self.total_checks} total combinations")

        if thread_count < 1:
            thread_count = 1

        o_count = len(self._offer_sets[0])
        thread_size = (o_count // thread_count)
        if thread_size < 1:
            thread_size = 1
        thread_intervals = list(range(0, o_count, thread_size))
        if len(thread_intervals) < thread_count + 1:
            thread_intervals += [o_count]
        else:
            thread_intervals = thread_intervals[:-1] + [o_count]
        thread_ranges = [list(range(thread_intervals[x], thread_intervals[x + 1])) for x in
                         range(len(thread_intervals) - 1)]

        threads = []
        for i, t_range in enumerate(thread_ranges):
            t_name = f"Thread_[{t_range[0]}-{t_range[-1]}]"
            thread = threading.Thread(target=self._find_lowest,
                                      args=[self._lowest_offer, 0, t_range],
                                      name=t_name,
                                      daemon=True)
            self._logger.info(f"Creating thread {t_name} ({i + 1}/{len(thread_ranges)})")
            threads.append(thread)

        for i, thread in enumerate(threads):
            self._logger.info(f"Starting thread {thread.name} ({i + 1}/{len(threads)})")
            thread.start()

        for thread in threads:
            thread.join()

        with self._lock:
            return self._lowest_offer

    def _find_lowest(self, reference_offers: OfferCollection, card_id: int, offer_range: Optional[list[int]] = None):
        if offer_range is None:
            offer_range = range(len(self._offer_sets[card_id]))
        card = self._offer_sets[card_id][0].card
        buf_offer = reference_offers.remove(card)
        offer_sets = self._offer_sets[card_id]

        for i in offer_range:
            offer = offer_sets[i]
            checked_offer = buf_offer.add(offer)
            if card_id < len(self._offer_sets) - 1:
                new_id = card_id + 1
                self._find_lowest(checked_offer, new_id)
            else:
                self._increment_check()
                self._update_lowest_offer(checked_offer)

    def _update_lowest_offer(self, offer: OfferCollection):
        with self._lock:
            if offer.sum() < self._lowest_offer.sum():
                self._logger.info(f"Replacing {self._lowest_offer.sum()} with {offer.sum()}")
                self._lowest_offer = offer
