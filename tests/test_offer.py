from card import Card
from offer import Offer
from seller import Seller

_card = Card("dummy_expansion", "dummy_card", 1)
_seller = Seller("dummy_seller", 1.15)
_amount = 13
_price = 22.68


def test_offer():
    offer = Offer(_card, _seller, _amount, _price)
    assert offer.card == _card
    assert offer.seller == _seller
    assert offer.amount == _amount
    assert offer.price == _price
