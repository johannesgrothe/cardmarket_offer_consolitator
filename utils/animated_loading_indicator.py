from typing import Any

from utils.loading_indicator import LoadingIndicator


class AnimatedLoadingIndicator(LoadingIndicator):
    _step: int
    _direction: bool
    _size: int
    _message: str

    def __init__(self, size: int = 5, message: str = "", *args: Any):
        super().__init__(message, *args)
        self._step = 0
        self._direction = True
        self._size = size
        self._message = " " + message.strip()

    def _thread_method(self) -> None:
        first_space = ' ' * self._step
        second_space = ' ' * (self._size - self._step)
        print(f"[{first_space}o{second_space}]{self._format_message()}{' ' * 40}", end="\r")
        if self._direction:
            self._step += 1
            if self._step == self._size:
                self._direction = False
        else:
            self._step -= 1
            if self._step == 0:
                self._direction = True
