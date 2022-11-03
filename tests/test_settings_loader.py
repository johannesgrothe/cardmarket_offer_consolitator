import os

from card_attributes import Language, SellerCountry, SellerType, CardCondition
from settings_loader import SettingsLoader


def test_settings_loader():
    data = SettingsLoader.load_settings(os.path.join("test_assets", "test_settings.json"))

    assert len(data.language) == 2
    assert Language.German in data.language
    assert Language.English in data.language

    assert len(data.seller_type) == 2
    assert SellerType.Private in data.seller_type
    assert SellerType.PowerSeller in data.seller_type

    assert data.seller_country == [SellerCountry.Germany]

    assert data.min_condition == CardCondition.LightlyPlayed
