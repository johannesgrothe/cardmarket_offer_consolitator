import pytest

from card import Card
from offer import Offer
from offer_set import OfferSet
from seller import Seller


@pytest.fixture
def f_card():
    return Card("expansion", "name", 4)


@pytest.fixture
def f_offers(f_card):
    return [
        Offer(f_card, Seller("seller4", 1.15), 2, .1),
        Offer(f_card, Seller("seller5", 1.15), 1, .1),
        Offer(f_card, Seller("seller6", 1.15), 2, .1)
    ]


def test_offer_set(f_offers, f_card):
    t_set = OfferSet(
        f_offers
    )
    sellers = t_set.sellers
    sellers.sort()
    assert sellers == [Seller("seller4", 1.15), Seller("seller6", 1.15)]

    assert t_set.card == f_card

    offers = t_set.offers
    offers.sort()
    assert offers == [Offer(f_card, Seller("seller4", 1.15), 2, .1),
                      Offer(f_card, Seller("seller6", 1.15), 2, .1)]
