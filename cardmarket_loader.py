import enum
import logging
import re
from bs4 import BeautifulSoup

import requests
from typing import Optional, List, Union

from card import Card
from offer import Offer
from seller import Seller
from settings_loader import SearchSettings

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
    _settings: SearchSettings

    def __init__(self, config: SearchSettings):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info(f"Creating CardmarketLoader")
        self._settings = config

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
        if self._settings.language:
            params["language"] = self._format_param(self._settings.language)
        if self._settings.min_condition:
            params["minCondition"] = self._format_param(self._settings.min_condition)
        if self._settings.seller_type:
            params["sellerType"] = self._format_param(self._settings.seller_type)
        if self._settings.seller_country:
            params["sellerCountry"] = self._format_param(self._settings.seller_country)
        return params

    @staticmethod
    def _check_for_errors(html: str, expansion: str) -> None:
        """
        Checks the html response for any displayed errors

        :param html: HTML-Code to parse
        :return: None
        :raises ExpansionError: If the website displays an expansion error
        :raises ProductError: If the website raises a prodict error
        """
        expansion_error = True if re.findall("class=\"alert-heading\">Fehler: Ungültige Erweiterung</", html) else False
        if expansion_error:
            raise ExpansionError(expansion)

        product_error = True if re.findall("class=\"alert-heading\">Ungültiges Produkt</", html) else False
        if product_error:
            raise ProductError(expansion)

    def _parse_offers(self, data: str, card: Card, expansion: str) -> List[Offer]:
        sellers = re.findall("<div id=\"(articleRow\\d+?)\" class=\".+? article-row\">",
                             data)
        offers = []
        for key in sellers:
            seller_data = BeautifulSoup(data, 'html.parser').find('div', id=key)
            str_data = str(seller_data)
            try:
                name = re.findall("<a href=\"/de/Magic/Users/(.+?)\">", str_data)
                count = re.findall("<span class=\"item-count small text-right\">(\\d+?)</span></div>", str_data)
                price = re.findall("\">(\\d+?,\\d+?) €</span>", str_data)
                name = name[0]
                count = int(count[0])
                price = float(price[0].replace(",", "."))
                offers.append(Offer(card, Seller(name, 1.15), count, price, expansion))
            except (IndexError, ValueError) as err:
                self._logger.error(err.args[0])
        return offers

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
        uris = [(self._build_uri(_base_url, exp, card.name), exp) for exp in card.expansions]
        # uri = self._build_uri(_base_url, card.expansion, card.name)
        params = self._prepare_params()
        all_offers = []
        for uri, expansion in uris:
            resp = requests.get(uri, params=params)
            if not resp.status_code == 200:
                raise DataLoadError(resp.status_code)

            self._check_for_errors(resp.text, expansion)

            self._logger.debug("Got response without errors")

            offers = self._parse_offers(resp.text, card, expansion)
            all_offers += offers
        return all_offers

    def find_expansion(self, card_id: str) -> List[str]:
        # https://www.cardmarket.com/de/Magic/Products/Search?searchString=Entdeckungen+der+Sippe
        uri = self._build_uri("https://www.cardmarket.com/de/Magic/Products/Search")
        params = {"searchString": card_id.replace(" ", "+")}
        resp = requests.get(uri, params=params)
        if not resp.status_code == 200:
            raise DataLoadError(resp.status_code)
        exp_data = re.findall("<a href=\"/de/Magic/Products/Singles/(.+?)/(.+?)\">.+?</a>", resp.text)
        return [x for x, y in exp_data]
