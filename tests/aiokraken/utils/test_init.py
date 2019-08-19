import pytest

from aiokraken.utils import get_kraken_logger, get_nonce


def test_get_nonce():
    """ Nonce counter.
    :returns: an always-increasing unsigned integer (up to 64 bits wide)
    """
    # call many time, verify always increasing integer (testing this properly can get tricky quickly...)
    d0 = get_nonce()
    d1 = get_nonce()

    assert d1 >= d0


def test_get_kraken_logger():
    """ Utility method for class specific logging
    """
    import logging

    # Setting up logger for test

    l = get_kraken_logger('testkraklog')

    assert l.level == logging.DEBUG
    assert l.propagate == True
    assert l.handlers and isinstance(l.handlers[0], logging.StreamHandler)


if __name__ == '__main__':
    pytest.main(['-s', __file__])
