"""Utility functions"""
import time
import logging

__all__ = ['get_kraken_logger', 'get_nonce']


def get_nonce():
    """ Nonce counter.
    :returns: an always-increasing unsigned integer (up to 64 bits wide)
    """
    return int(1000 * time.time())


def get_kraken_logger(name):
    """ Utility method for class specific logging
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = True
    if not logger.handlers:
        # Add console log
        console = logging.StreamHandler()
        formatter_console = logging.Formatter(
            '%(asctime)s %(levelname) -10s %(name) -10s'
            ' %(funcName) -10s %(lineno) -5d  %(message)s'
        )
        console.setFormatter(formatter_console)
        console.setLevel(logging.INFO)
        logger.addHandler(console)
    return logger

