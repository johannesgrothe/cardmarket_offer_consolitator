import threading
import time
from typing import Optional, Any

from utils.loading_indicator import LoadingIndicator


class FormattedLoadingIndicator(LoadingIndicator):
    _running: bool
    _run_thread: Optional[threading.Thread]
    _format_string: str
    _args: Any

    def __init__(self, format_string: str, *args):
        self._running = False
        self._run_thread = None
        self._format_string = format_string
        self._args = args

    def __del__(self):
        self.stop()

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.stop()

    def _thread_runner(self):
        while self._running:
            print(self._format_string.format(*self._args), end="\r")
            time.sleep(0.1)

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
