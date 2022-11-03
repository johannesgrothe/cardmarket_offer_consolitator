from typing import Optional

from card_attributes import CardCondition, Language, SellerType, SellerCountry


class SearchSettings:
    min_condition: Optional[CardCondition]
    language: list[Language]
    seller_type: list[SellerType]
    seller_country: list[SellerCountry]

    def __init__(self, language: Optional[list[Language]] = None, min_condition: Optional[CardCondition] = None,
                 seller_country: Optional[list[SellerCountry]] = None, seller_type: Optional[list[SellerType]] = None):
        self.min_condition = min_condition
        self.language = language if language else []
        self.seller_type = seller_type if seller_country else []
        self.seller_country = seller_country if seller_type else []
