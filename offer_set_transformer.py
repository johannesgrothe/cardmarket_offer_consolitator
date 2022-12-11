import logging

from card import Card
from offer import Offer
from offer_set import OfferSet
from set_creator import OfferSetCreator


class OfferSetTransformer:
    _logger: logging.Logger
    _data: dict[Card, list[OfferSet]]

    def __init__(self, in_data: dict[Card, list[Offer]]):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._data = self._transform_to_sets(in_data)

    @property
    def data(self):
        return self._data

    def _transform_to_sets(self, in_data: dict[Card, list[Offer]]) -> dict[Card, list[OfferSet]]:
        out_data: dict[Card, list[OfferSet]] = {}
        for card, offers in in_data.items():
            out_data[card] = OfferSetCreator(offers).sets
            self._logger.info(f"Created {len(out_data[card])} offer-sets for '{card.name}'")
        return out_data
