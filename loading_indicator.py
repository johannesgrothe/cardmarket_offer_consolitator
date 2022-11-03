import threading
import time
from typing import Optional, Callable, Tuple


class LoadingIndicator:
    _running: bool
    _run_thread: Optional[threading.Thread]
    _status_info: Optional[Tuple[int, Callable[[], int]]]
    _step: int
    _direction: bool
    _size: int

    def __init__(self, status_info: Optional[Tuple[int, Callable[[], int]]] = None, size: int = 5):
        self._running = False
        self._run_thread = None
        self._status_info = status_info
        self._step = 0
        self._direction = True
        self._size = size

    def __del__(self):
        self.stop()

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.stop()

    def _thread_runner(self):
        while self._running:
            status_part = ""
            if self._status_info:
                total = self._status_info[0]
                current = self._status_info[1]()
                percent = round(current / total * 100)
                status_part = f"| {current}/{total} | {percent}%"
            first_space = ' ' * self._step
            second_space = ' ' * (self._size - self._step)
            print(f"[{first_space}o{second_space}{status_part}]{' ' * 15}",
                  end="\r")
            if self._direction:
                self._step += 1
                if self._step == self._size:
                    self._direction = False
            else:
                self._step -= 1
                if self._step == 0:
                    self._direction = True
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
