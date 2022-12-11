import logging

from card import Card
from offer import Offer


class OfferFilter:
    _logger: logging.Logger
    _data: dict[Card, list[Offer]]

    def __init__(self, data: dict[Card, list[Offer]]):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._data = data
        self._data = self._remove_single_sellers(self._data)
        self._data = self._remove_expensive_offers(self._data)

    @property
    def data(self) -> dict[Card, list[Offer]]:
        return self._data

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
            if card.amount > 1:
                out_data[card] = offers
                continue
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
