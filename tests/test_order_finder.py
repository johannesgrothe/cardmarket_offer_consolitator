import pytest

from card import Card
from offer import Offer
from offer_collection import OfferCollection
from offer_set import OfferSet
from offer_set_transformer import OfferSetTransformer
from order_finder import OrderFinder
from seller import Seller

_card1 = Card("expansion-1", "card-1", 2)
_card2 = Card(["expansion-1", "expansion-2"], "card-2", 1)
_card3 = Card("expansion-3", "card-3", 1)
_seller1 = Seller("seller-1", 1.15)
_seller2 = Seller("seller-2", 1.15)
_seller3 = Seller("seller-3", 1.15)
_seller4 = Seller("seller-4", 1.15)
_seller5 = Seller("seller-5", 1.15)
_seller6 = Seller("seller-6", 1.15)
_seller7 = Seller("seller-7", 1.15)
_seller8 = Seller("seller-8", 1.15)


@pytest.fixture
def f_all_offers() -> dict[Card, list[OfferSet]]:
    offers = {
        _card1: [Offer(_card1, _seller1, 1, 0.10, "expansion-1"),
                 Offer(_card1, _seller2, 1, 0.12, "expansion-1"),
                 Offer(_card1, _seller3, 2, 0.30, "expansion-1"),
                 Offer(_card1, _seller4, 4, 0.34, "expansion-1")],
        _card2: [Offer(_card2, _seller5, 1, 0.40, "expansion-1"),
                 Offer(_card2, _seller6, 1, 0.48, "expansion-1")],
        _card3: [Offer(_card3, _seller8, 1, 0.47, "expansion-1"),
                 Offer(_card3, _seller6, 1, 0.55, "expansion-1"),
                 Offer(_card3, _seller7, 1, 1.10, "expansion-1")]
    }
    return OfferSetTransformer(offers).data


@pytest.mark.parametrize("thread_count", [-1, 0, 1, 2, 3, 4, 5, 10000])
def test_order_finder(f_all_offers, thread_count):
    finder = OrderFinder(f_all_offers)
    result = finder.find_lowest_offer(thread_count)
    assert result == OfferCollection([
        OfferSet([Offer(_card1, _seller3, 2, 0.30, "expansion-1")]),
        OfferSet([Offer(_card2, _seller6, 1, 0.48, "expansion-1")]),
        OfferSet([Offer(_card3, _seller6, 1, 0.55, "expansion-1")])
    ])
    assert finder.performed_checks == finder.total_checks
