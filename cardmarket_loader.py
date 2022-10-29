import enum
import logging
import re
from bs4 import BeautifulSoup

import requests
from typing import Optional, List, Union

from card_attributes import Language, CardCondition, SellerCountry, SellerType

_base_url = "https://www.cardmarket.com/de/Magic/Products/Singles"


class Offer:
    _seller: str
    _amount: int
    _price: float

    def __init__(self, seller: str, amount: int, price: float):
        self._seller = seller
        self._amount = amount
        self._price = price

    def __str__(self):
        return f"{self._seller}: {self._amount} for {self._price}"

    @property
    def seller(self) -> str:
        return self._seller

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def price(self) -> float:
        return self._price


class CardmarketLoader:
    _logger: logging.Logger
    _language: Optional[Language]
    _min_condition: Optional[CardCondition]
    _seller_country: List[SellerCountry]
    _seller_type: List[SellerType]

    def __init__(self, language: Optional[Language] = None, min_condition: Optional[CardCondition] = None,
                 seller_country: Optional[List[SellerCountry]] = None, seller_type: Optional[List[SellerType]] = None):
        self._logger = logging.getLogger(self.__class__.__name__)
        if seller_country is None:
            seller_country = []
        if seller_type is None:
            seller_type = []
        self._language = language
        self._min_condition = min_condition
        self._seller_country = seller_country
        self._seller_type = seller_type

    @staticmethod
    def _build_uri(base_uri: str, *args: str) -> str:
        out = base_uri.strip("/")
        for arg in args:
            out += "/" + arg.strip("/")
        return out

    @staticmethod
    def _format_param(param: Union[List[enum.IntEnum], Union[enum.IntEnum]]) -> str:
        if isinstance(param, List):
            return str([x.value for x in param]).strip("]").strip("[")
        return str(param.value)

    def _prepare_params(self) -> dict:
        params = {}
        if self._language:
            params["language"] = self._format_param(self._language)
        if self._min_condition:
            params["minCondition"] = self._format_param(self._min_condition)
        if self._seller_type:
            params["sellerType"] = self._format_param(self._seller_type)
        if self._seller_country:
            params["sellerCountry"] = self._format_param(self._seller_country)
        return params

    def load_card(self, edition: str, name: str) -> List[Offer]:
        uri = self._build_uri(_base_url, edition, name)
        params = self._prepare_params()
        resp = requests.get(uri, params=params)
        if not resp.status_code == 200:
            raise ConnectionError()

        sellers = re.findall("<div id=\"(articleRow\\d+?)\" class=\".+? article-row\">",
                             resp.text)
        offers = []
        for key in sellers:
            seller_data = BeautifulSoup(resp.text, 'html.parser').find('div', id=key)
            str_data = str(seller_data)
            try:
                name = re.findall("<a href=\"/de/Magic/Users/(.+?)\">", str_data)
                count = re.findall("<span class=\"item-count small text-right\">(\\d+?)</span></div>", str_data)
                price = re.findall("\">(\\d+?,\\d+?) €</span>", str_data)
                name = name[0]
                count = int(count[0])
                price = float(price[0].replace(",", "."))
                offers.append(Offer(name, count, price))
            except (IndexError, ValueError) as err:
                self._logger.info(err.args[0])

        return offers
