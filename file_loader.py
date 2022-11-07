import logging
import os.path
from typing import List, Callable, Optional, Union

from card import Card


class FileLoader:
    _logger: logging.Logger
    _file: str
    _print_callback: Optional[Callable[[str], None]]

    _double_cards: int
    _illegal_identifiers: int

    _cards: List[Card]

    def __init__(self, filepath: str, print_callback: Optional[Callable[[str], None]] = None):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._file = os.path.realpath(filepath)
        self._print_callback = print_callback
        self._double_cards = 0
        self._illegal_identifiers = 0
        if not os.path.isfile(self._file):
            raise FileNotFoundError()
        self._logger.info(f"Created file loader for {self._file}")
        self._cards = self._parse()

    @property
    def file(self) -> str:
        return self._file

    @property
    def double_cards(self) -> int:
        """The amount of double cards found in the file"""
        return self._double_cards

    @property
    def illegal_identifiers(self) -> int:
        """The amount of illegal identifiers found in the file"""
        return self._illegal_identifiers

    @property
    def cards(self) -> List[Card]:
        return self._cards

    def _log_err(self, msg: str):
        self._logger.error(msg)
        if self._print_callback is not None:
            self._print_callback(msg)

    def _parse(self) -> List[Card]:
        cards = []
        with open(self._file, "r") as file_p:
            for i, line in enumerate([x.strip("\n").strip("\r") for x in file_p.readlines()]):
                if not line:
                    continue
                parts: list[Union[str, int]] = [x for x in [x.strip() for x in line.split("/")] if x]
                try:
                    parts[-1] = int(parts[-1])
                except ValueError:
                    pass

                try:
                    if len(parts) == 2:
                        expansion, name = parts
                        amount = 1
                        if isinstance(name, int):
                            raise ValueError()
                    elif len(parts) == 3:
                        expansion, name, amount = parts
                    else:
                        raise ValueError()
                except ValueError:
                    self._log_err(f"Illegal Card Identifier in line {i + 1}: '{line}'")
                    self._illegal_identifiers += 1
                    continue

                parsed_card = Card(expansion, name, amount)
                if parsed_card in cards:
                    self._log_err(f"Double Card in line {i + 1}: '{parsed_card}'")
                    self._double_cards += 1
                    continue
                cards.append(parsed_card)

        self._logger.info(f"{len(cards)} cards read from file")
        return cards
