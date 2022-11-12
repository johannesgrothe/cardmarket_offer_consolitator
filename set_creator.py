from offer import Offer
from offer_set import OfferSet


class OfferSetCreator:
    _offers: list[Offer]
    _sets: list[OfferSet]

    def __init__(self, offers: list[Offer]):
        self._offers = offers
        for offer in self._offers:
            if offer.card != self._offers[0].card:
                raise ValueError("All Offers must be for the same Card")
        self._sets = []
        self._create_sets()
        self._remove_doubles()

    @property
    def sets(self) -> list[OfferSet]:
        return self._sets

    def _remove_doubles(self):
        out_data = []
        for x in self._sets:
            if x not in out_data:
                out_data.append(x)
        self._sets = out_data

    def _create_set(self, elem: OfferSet) -> None:
        if elem.cards_available >= elem.card.amount:
            self._sets.append(elem)
            return
        for offer in [x for x in self._offers if x not in elem.offers]:
            self._create_set(OfferSet(elem.offers + [offer]))

    def _create_sets(self) -> None:
        for offer in self._offers:
            self._create_set(OfferSet([offer]))
