import pytest

from card import Card
from offer import Offer
from seller import Seller
from set_creator import OfferSetCreator


@pytest.fixture
def f_card():
    return Card("expansion", "name", 4)


@pytest.fixture
def f_offers(f_card):
    return [
        Offer(f_card, Seller("seller1", 1.15), 1, .10),
        Offer(f_card, Seller("seller2", 1.15), 1, .10),
        Offer(f_card, Seller("seller3", 1.15), 1, .30),
        Offer(f_card, Seller("seller4", 1.15), 1, .20),
        Offer(f_card, Seller("seller5", 1.15), 2, .32),
        Offer(f_card, Seller("seller6", 1.15), 2, .12),
        Offer(f_card, Seller("seller7", 1.15), 3, .17),
        Offer(f_card, Seller("seller8", 1.15), 4, .10),
        Offer(f_card, Seller("seller9", 1.15), 5, .12)
    ]


def test_set_creator(f_offers):
    creator = OfferSetCreator(f_offers)
    assert len(creator.sets) > 0
