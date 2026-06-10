from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from ...core import settings


class ThreadingService:
    def __init__(self):
        self.max_workers = settings.WORKER_POOL_SIZE
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)

        self.active_tasks = 0
        self.lock = Lock()

    def get_active_tasks(self):
        with self.lock:
            return self.active_tasks

    def is_full(self):
        return self.get_active_tasks() >= self.max_workers

    def run(self, func, *args, **kwargs):
        def wrapper():
            try:
                return func(*args, **kwargs)
            finally:
                with self.lock:
                    self.active_tasks -= 1

        with self.lock:
            self.active_tasks += 1

        return self.executor.submit(wrapper)

    def shutdown(self):
        self.executor.shutdown(wait=True)

    def wait(self):
        self.executor.shutdown(wait=True)
