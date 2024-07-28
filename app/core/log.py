import logging


# TODO: logging config
Logger = logging.Logger
FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


def GetLogger(name: str | None = None) -> Logger:
    return logging.getLogger(name)
