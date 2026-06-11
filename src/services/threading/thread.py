from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from src.core.configs import Settings


class ThreadingService:

    def __init__(self, settings: Settings) -> None:
        self.max_workers = settings.WORKER_POOL_SIZE
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)

        self.active_tasks = 0
        self._lock = Lock()

    def get_active_tasks(self) -> int:
        with self._lock:
            return self.active_tasks

    def is_full(self) -> bool:
        return self.get_active_tasks() >= self.max_workers

    def run(self, func, *args, **kwargs) -> None:
        """
        Submits func to the thread pool.
        active_tasks is incremented before and decremented in the finally block,
        ensuring correct counting even in case of an exception.
        """
        def wrapper():
            try:
                func(*args, **kwargs)
            finally:
                with self._lock:
                    self.active_tasks -= 1

        with self._lock:
            self.active_tasks += 1

        self.executor.submit(wrapper)

    def shutdown(self, wait: bool = True) -> None:
        self.executor.shutdown(wait=wait)