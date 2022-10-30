import pytest

from card import Card
from card_attributes import Language, CardCondition, SellerCountry, SellerType
from cardmarket_loader import CardmarketLoader, DataLoadError, ProductError, ExpansionError


@pytest.fixture()
def f_empty_loader():
    return CardmarketLoader()


def test_uri_builder():
    built_uri = CardmarketLoader._build_uri("http://blub.com/", "blub1", "blub2", "/blub3/")
    assert built_uri == "http://blub.com/blub1/blub2/blub3"


def test_param_format():
    loader = CardmarketLoader(language=Language.German,
                              min_condition=CardCondition.Excellent,
                              seller_country=[SellerCountry.Germany],
                              seller_type=[SellerType.Private])
    param_dict = loader._prepare_params()
    assert len(param_dict.keys()) == 4

    loader = CardmarketLoader(seller_country=[SellerCountry.Germany],
                              seller_type=[SellerType.Private])
    param_dict = loader._prepare_params()
    assert len(param_dict.keys()) == 2

    loader = CardmarketLoader(language=Language.German,
                              min_condition=CardCondition.Excellent)
    param_dict = loader._prepare_params()
    assert len(param_dict.keys()) == 2


def test_card_load(f_empty_loader):
    offers = f_empty_loader.load_offers_for_card(Card(expansion="Born-of-the-Gods", name="Plea-for-Guidance"))
    assert len(offers) > 0


def test_card_load_product_error(f_empty_loader):
    with pytest.raises(ProductError):
        f_empty_loader.load_offers_for_card(Card(expansion="Born-of-the-Gods", name="bongobob"))


def test_card_load_expansion_error(f_empty_loader):
    with pytest.raises(ExpansionError):
        f_empty_loader.load_offers_for_card(Card(expansion="bongobob", name="Plea-for-Guidance"))
