import logging
import os.path
from typing import List, Callable, Optional

from card import Card


class FileLoader:
    _logger: logging.Logger
    _file: str
    _print_callback: Optional[Callable[[str], None]]

    def __init__(self, filepath: str, print_callback: Optional[Callable[[str], None]] = None):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._file = os.path.realpath(filepath)
        self._print_callback = print_callback
        if not os.path.isfile(self._file):
            raise FileNotFoundError()
        self._logger.info(f"Created file loader for {self._file}")

    @property
    def file(self) -> str:
        return self._file

    def _log_err(self, msg: str):
        self._logger.error(msg)
        if self._print_callback is not None:
            self._print_callback(msg)

    def parse(self) -> List[Card]:
        cards = []
        with open(self._file, "r") as file_p:
            for i, line in enumerate([x.strip("\n").strip("\r") for x in file_p.readlines()]):
                if not line:
                    continue
                try:
                    expansion, name = [x.strip() for x in line.split("/")]
                except ValueError:
                    self._log_err(f"Illegal Card Identifier in line {i+1}: '{line}'")
                    continue
                parsed_card = Card(expansion, name)
                if parsed_card in cards:
                    self._log_err(f"Double Card in line {i+1}: '{parsed_card}'")
                    continue
                cards.append(parsed_card)

        self._logger.info(f"{len(cards)} cards read from file")
        return cards
