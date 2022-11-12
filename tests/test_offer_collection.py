import pytest

from card import Card
from offer import Offer
from offer_collection import OfferCollection
from offer_set import OfferSet
from seller import Seller

seller1 = Seller("seller1", 1.40)
seller2 = Seller("seller2", 1.15)
seller3 = Seller("seller3", 1.15)


@pytest.fixture
def f_offers():
    offers = [Offer(Card(f"expansion1", f"card1"), seller1, 1, 0.1),
              Offer(Card(f"expansion2", f"card2"), seller2, 1, 0.2),
              Offer(Card(f"expansion3", f"card3"), seller3, 1, 0.3),
              Offer(Card(f"expansion00", f"card00a"), seller2, 1, 0.02),
              Offer(Card(f"expansion00", f"card00b"), seller2, 1, 1.05)]
    offer_sets = [OfferSet([x]) for x in offers]
    return OfferCollection(offer_sets)


def test_offer_collection_sum(f_offers):
    assert round(f_offers.sum(), 4) == round(0.1 + 0.2 + 0.3 + 0.02 + 1.05 + 1.40 + 1.15 + 1.15, 4)


def test_offer_collection_seller(f_offers):
    sellers = f_offers.sellers
    assert len(sellers) == 3
    assert seller1 in sellers
    assert seller2 in sellers
    assert seller3 in sellers
