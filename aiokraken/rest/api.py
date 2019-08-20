import urllib
import hashlib
import base64
import hmac
import time
import signal
import asyncio

from dataclasses import dataclass, asdict, field

import typing

if __package__:
    from .request import Request
    from ..utils import get_nonce, get_kraken_logger
else:
    from aiokraken.rest.request import Request
    from aiokraken.utils import get_nonce, get_kraken_logger


class API:

    def __init__(self, base_url_path):
        self.base_url_path =base_url_path
        self.api_url = 'public/'

    @property
    def url_path(self):
        return self.base_url_path + self.api_url

    def headers(self, endpoint= None):
        _headers = {
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
            )
        }

        return _headers

    def request(self, endpoint, headers=None, data=None):
        h = headers or {}
        r = Request(url=self.url_path + endpoint, headers=h, data=data)

        return r


class Private:

    def __init__(self, base_url_path, key, secret):
        self.base_url_path = base_url_path
        self.api_url = 'private/'

        # TODO :call function (arg) to grab them from somewhere...
        self.key = key
        self.secret = secret

    @property
    def url_path(self):
        return self.base_url_path + self.api_url

    def headers(self, endpoint= None):
        _headers = {
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
            )
        }

        return _headers

    def _sign_message(self, data, url_path):
        """
            Kraken message signature for private user endpoints
            https://www.kraken.com/features/api#general-usage
        """
        post_data = urllib.parse.urlencode(data)

        # Unicode-objects must be encoded before hashing
        encoded = (str(data['nonce']) + post_data).encode()
        message = url_path.encode() + hashlib.sha256(encoded).digest()
        signature = hmac.new(
            base64.b64decode(self.secret),
            message,
            hashlib.sha512
        )
        sig_digest = base64.b64encode(signature.digest())

        return sig_digest.decode()

    def sign(self, req: Request):
        req.data['nonce'] = get_nonce()
        req.headers['API-Key'] = self.key
        req.headers['API-Sign'] = self._sign_message(req.data, req.url)

        return req

    def request(self, endpoint, headers=None, data=None):
        h = headers or {}
        d = data or {}
        r = Request(url=self.url_path + endpoint, headers=h, data=d)
        s = self.sign(r)
        return s


class Server:
    """ Class representing a SErver API"""

    def __init__(self, key=None, secret=None):
        self.key = key
        self.secret = secret
        self.versions = ['0']
        self.current_version = self.versions[0]
        self._public = None
        self._private = None

    @property
    def url_path(self):
        return '/' + self.current_version + '/'

    @property
    def public(self):
        if self._public is None:
            self._public = API(base_url_path=self.url_path)
        return self._public

    @property
    def private(self):
        if self._private is None:
            self._private = Private(base_url_path=self.url_path, key = self.key, secret=self.secret)
        return self._private

    def time(self):
        return self.public.request('Time', data=None)

    def balance(self):
        return self.private.request('Balance', data=None)


import aiohttp

LOGGER = get_kraken_logger(__name__)


# MINIMAL CLIENT (only control flow & IO)
class RestClient:

    def __init__(self, host, api, protocol = "https://"):
        self.host = host
        self.api = api
        self.protocol = protocol

        _headers = {
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
            )
        }

        self.session = aiohttp.ClientSession(headers=_headers, raise_for_status=True, trust_env=True)

    async def time(self):
        """ make public requests to kraken api"""

        kt = self.api.time()

        try:  # TODO : pass protocol & host into the request url in order to have it displayed when erroring !
            async with self.session.post(self.protocol + self.host + kt.url, headers=kt.headers, data=kt.data) as response:

                return await kt(response)

        except aiohttp.ClientResponseError as err:
            LOGGER.error(err)
            return {'error': err}

    async def balance(self):
        """ make public requests to kraken api"""

        kt = self.api.balance()

        try:
            async with self.session.post(self.protocol + self.host + kt.url, headers=kt.headers, data=kt.data) as response:

                return await kt(response)

        except aiohttp.ClientResponseError as err:
            LOGGER.error(err)
            return {'error': err}



    async def close(self):
        """ Close aiohttp session """
        await self.session.close()


# API DEFINITION

# @kraken.resource(success = , error=)
# def time(headers, data):
#     return {
#         200: success,
#         400: error,
#     }


# EXAMPLE CODE


async def get_time():
    """ get kraken time"""
    rest_kraken = RestClient(host='api.kraken.com', api = Server())
    try:
        response = await rest_kraken.time()
        print(f'response is {response}')
    finally:
        await rest_kraken.close()


async def get_balance():
    """Start kraken websockets api
    """
    from aiokraken.rest import krak_key
    rest_kraken = RestClient(host='api.kraken.com',
                             api = Server(key=krak_key.key,
                                          secret=krak_key.secret))
    response = await rest_kraken.balance()
    await rest_kraken.close()
    print(f'response is {response}')


@asyncio.coroutine
def ask_exit(sig_name):
    print("got signal %s: exit" % sig_name)
    yield from asyncio.sleep(1.0)
    asyncio.get_event_loop().stop()


loop = asyncio.get_event_loop()


for signame in ('SIGINT', 'SIGTERM'):
    loop.add_signal_handler(
        getattr(signal, signame),
        lambda: asyncio.ensure_future(ask_exit(signame))
    )

#loop.run_until_complete(get_time())
loop.run_until_complete(get_balance())
