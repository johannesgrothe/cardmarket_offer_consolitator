import enum
import logging
import re
from bs4 import BeautifulSoup

import requests
from typing import Optional, List, Union

from card import Card
from card_attributes import Language, CardCondition, SellerCountry, SellerType
from offer import Offer

_base_url = "https://www.cardmarket.com/de/Magic/Products/Singles"


class DataLoadError(Exception):
    code: int

    def __init__(self, code: int, msg: Optional[str] = None):
        if msg is None:
            msg = f"Server returned non-200 status code {code}"
        super().__init__(msg)
        self.code = code


class ProductError(Exception):
    pass


class ExpansionError(Exception):
    pass


class CardmarketLoader:
    _logger: logging.Logger
    _language: Optional[Language]
    _min_condition: Optional[CardCondition]
    _seller_country: List[SellerCountry]
    _seller_type: List[SellerType]

    def __init__(self, language: Optional[Language] = None, min_condition: Optional[CardCondition] = None,
                 seller_country: Optional[List[SellerCountry]] = None, seller_type: Optional[List[SellerType]] = None):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info(f"Creating CardmarketLoader")
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

    @staticmethod
    def _check_for_errors(html: str) -> None:
        """
        Checks the html response for any displayed errors

        :param html: HTML-Code to parse
        :return: None
        :raises ExpansionError: If the website displays an expansion error
        :raises ProductError: If the website raises an prodict error
        """
        expansion_error = True if re.findall("class=\"alert-heading\">Fehler: Ungültige Erweiterung</", html) else False
        if expansion_error:
            raise ExpansionError()

        product_error = True if re.findall("class=\"alert-heading\">Ungültiges Produkt</", html) else False
        if product_error:
            raise ProductError()

    def load_offers_for_card(self, card: Card) -> List[Offer]:
        """
        Loads the offers for the selected card from cardmarket

        :param card: Card to look for
        :return: List of all offers
        :raises DataLoadError: If loading the data fails for any reason
        :raises ExpansionError: If The expansion of the card is not legal
        :raises ProductError: If the card does not exist
        """
        self._logger.info(f"Loading offers for '{card}'")
        uri = self._build_uri(_base_url, card.expansion, card.name)
        params = self._prepare_params()
        resp = requests.get(uri, params=params)
        if not resp.status_code == 200:
            raise DataLoadError(resp.status_code)

        self._check_for_errors(resp.text)

        self._logger.debug("Got response without errors")

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
                self._logger.error(err.args[0])
        return offers
