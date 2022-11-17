import pytest

from card import Card
from cardmarket_loader import CardmarketLoader
from offer import Offer
from order_finder import OrderFinder
from search_settings import SearchSettings
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
def f_all_offers() -> dict[Card, list[Offer]]:
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
    return offers


def test_order_finder(f_all_offers):
    finder = OrderFinder(f_all_offers)
    result = finder.find_lowest_offer()
    assert result
