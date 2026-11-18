import logging
from pathlib import Path


class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level):
        super().__init__()
        self.max_level = max_level

    def filter(self, record):
        return record.levelno < self.max_level


def logger_init():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    default_handler = logging.FileHandler(log_dir / "logs.txt", encoding="utf-8")
    default_handler.setLevel(logging.INFO)
    default_handler.addFilter(MaxLevelFilter(logging.ERROR))
    default_handler.setFormatter(formatter)

    error_handler = logging.FileHandler(log_dir / "error_logs.txt", encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    logger.addHandler(default_handler)
    logger.addHandler(error_handler)

    return logger
