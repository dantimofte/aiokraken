import pytest

from aiokraken.rest.upl import k

@pytest.mark.vcr()
def test_time():
    response = k.get_time()
    print(response)
    # asserting structure (but marshmallow could do it)
    assert not response.get('error')
    assert response.get('result').get('rfc1123')
    assert response.get('result').get('unixtime')


if __name__ == '__main__':
    pytest.main(['-s', __file__])
