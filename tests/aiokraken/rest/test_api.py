import pytest

from aiokraken.rest.api import Request


def test_request():

    r = Request(url='proto://some/url', headers={}, data={})

    assert hasattr(r, 'url')
    assert hasattr(r, 'headers')
    assert hasattr(r, 'data')


@pytest.mark.vcr()
def test_iana():
    response = urlopen('http://www.iana.org/domains/reserved').read()
    assert b'Example domains' in response



if __name__ == '__main__':
    pytest.main(['-s', __file__])
