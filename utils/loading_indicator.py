import threading
import time
from abc import abstractmethod, ABCMeta
from typing import Optional


class LoadingIndicator(metaclass=ABCMeta):
    _running: bool
    _run_thread: Optional[threading.Thread]
    _message: str

    def __init__(self, message: str):
        self._running = False
        self._run_thread = None
        self._message = message

    def __del__(self):
        self.stop()

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.stop()

    def _format_message(self) -> str:
        return self._message

    def _thread_runner(self):
        while self._running:
            self._thread_method()
            time.sleep(0.1)

    @abstractmethod
    def _thread_method(self) -> None:
        pass

    def _stop_thread(self):
        self._running = False
        if self._run_thread:
            self._run_thread.join()

    def run(self):
        self._stop_thread()
        self._running = True
        self._run_thread = threading.Thread(target=self._thread_runner)
        self._run_thread.name = self.__class__.__name__
        self._run_thread.start()

    def stop(self):
        if self._running:
            self._stop_thread()
        print(" " * 90, end="\r")
