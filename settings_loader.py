import json

from card_attributes import Language, CardCondition, SellerType, SellerCountry
from search_settings import SearchSettings


class SettingsLoader:

    @classmethod
    def load_settings(cls, file: str) -> SearchSettings:
        with open(file, "r") as file_p:
            config = json.load(file_p)

        for key in ["language", "seller_type", "seller_country"]:
            if not isinstance(config[key], list) and config[key] is not None:
                config[key] = [config[key]]

        out = SearchSettings()

        if config["language"]:
            out.language = [Language(x) for x in config["language"]]

        if config["seller_type"]:
            out.seller_type = [SellerType(x) for x in config["seller_type"]]

        if config["seller_country"]:
            out.seller_country = [SellerCountry(x) for x in config["seller_country"]]

        if config["min_condition"]:
            out.min_condition = CardCondition(config["min_condition"])

        return out
