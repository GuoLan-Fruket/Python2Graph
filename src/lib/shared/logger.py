import logging

_LOGGER = logging.getLogger("py2graph")
_LOGGER.setLevel(logging.DEBUG)
_LOGGER.addHandler(logging.StreamHandler())


def logger():
    return _LOGGER


def set_log_level(level):
    level = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }.get(level, logging.INFO)
    _LOGGER.setLevel(level)
