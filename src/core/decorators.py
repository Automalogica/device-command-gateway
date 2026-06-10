import logging
import time


def execution_time(func):
    logger = logging.getLogger(func.__name__)

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(
            f"Function/Class started | time={end_time - start_time:.2f}s"
        )
        return result

    return wrapper
