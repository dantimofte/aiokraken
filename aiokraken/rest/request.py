import hashlib
import hmac
import urllib
import base64
from dataclasses import dataclass, asdict, field
from ..utils import get_nonce
import typing

"""
A dataclass representing a request
"""
def _sign_message(data, url_path, secret):
    """
        Kraken message signature for private user endpoints
        https://www.kraken.com/features/api#general-usage
        url_path starts from the root (like "/<version>/private/endpoint")
    """
    post_data = urllib.parse.urlencode(data)

    # Unicode-objects must be encoded before hashing
    encoded = (str(data['nonce']) + post_data).encode()
    message = url_path.encode() + hashlib.sha256(encoded).digest()
    signature = hmac.new(
        base64.b64decode(secret),
        message,
        hashlib.sha512
    )
    sig_digest = base64.b64encode(signature.digest())

    return sig_digest.decode()


@dataclass(frozen=False)
class Request:
    """
    Request : Mutable or immutable ? (with state monad style management ?)
    Idempotent call (or 'retry' semantic ? based on error code ?)
    """

    url: str = ""
    data: typing.Dict = field(default_factory=dict)
    headers: typing.Dict = field(default_factory=dict)

    async def __call__(self, response):
        """
        Locally modelling the request.
        returning possible responses, and how to deal with them
        :return:
        """

        if response.status not in (200, 201, 202):
            return {
                'request': asdict(self),
                'error': response.status}
        else:
            res = await response.json(encoding='utf-8', content_type=None)
            res['request'] = asdict(self),
            res['error'] = "" if 'error' not in res else res['error']
            return res

    def sign(self, key, secret):
        self.data['nonce'] = get_nonce()
        self.headers['API-Key'] = key
        self.headers['API-Sign'] = _sign_message(self.data, self.url, secret)

        return self


