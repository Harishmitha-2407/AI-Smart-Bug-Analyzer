"""
utils/logger.py
---------------
Centralised logger factory used by every module in the project.
"""

import logging
import sys
import config


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured :class:`logging.Logger` for *name*.

    The handler is added only once per logger so repeated imports
    do not produce duplicate log lines.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

    level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)
    return logger
