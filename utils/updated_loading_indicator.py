from typing import Callable, Any

from utils.loading_indicator import LoadingIndicator


class UpdatedLoadingIndicator(LoadingIndicator):
    _max_value: int
    _current_value: Callable[[], int]
    _precision: int
    _message: str

    def __init__(self, max_value: int, current_value: Callable[[], int], precision: int = 0, message: str = ""):
        super().__init__(message)
        self._max_value = max_value
        self._current_value = current_value
        self._precision = precision
        self._message = " " + message.strip()

    def _thread_method(self) -> None:
        total = self._max_value
        current = self._current_value()
        percent = round(current / total * 100, self._precision)
        print(f"[{percent}%]{self._format_message()}{' ' * 40}", end="\r")
