from card import Card

_exp = "test_expansion"
_name = "test_name"


def test_card():
    card = Card(_exp, _name)
    assert card.expansion == _exp
    assert card.name == _name
