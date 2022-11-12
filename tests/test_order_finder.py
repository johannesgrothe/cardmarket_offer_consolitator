import pytest

from card import Card
from cardmarket_loader import CardmarketLoader
from order_finder import OrderFinder
from search_settings import SearchSettings


@pytest.fixture
def f_all_cards():
    return [
        Card("Theros-Beyond-Death-Extras", "Goat-Token-White-01", 2),
        Card("Commander-Legends-Battle-for-Baldurs-Gate-Extras", "Copy-Token", 2),
        Card("Amonkhet", "Warrior-Token-White-11-Vigilance", 1),
        # Card("Born-of-the-Gods", "Plea-for-Guidance", 1),
        # Card("Eternal-Masters", "Enlightened-Tutor", 1),
        Card("Theros-Beyond-Death", "Idyllic-Tutor", 1)
    ]


@pytest.fixture
def f_all_offers(f_all_cards):
    loader = CardmarketLoader(SearchSettings())
    return {
        card: loader.load_offers_for_card(card) for card in f_all_cards
    }


def test_order_finder(f_all_offers):
    finder = OrderFinder(f_all_offers)
    result = finder.find_lowest_offer()
    assert result
