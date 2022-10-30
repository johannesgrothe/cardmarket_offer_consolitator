from offer import Offer

_seller = "test_seller"
_amount = 13
_price = 22.68


def test_offer():
    offer = Offer(_seller, _amount, _price)
    assert offer.seller == _seller
    assert offer.amount == _amount
    assert offer.price == _price
