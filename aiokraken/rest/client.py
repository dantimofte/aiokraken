""" AIOKraken rest client """
import urllib
import hashlib
import hmac
import base64
import aiohttp
from aiokraken.utils import get_kraken_logger, get_nonce

BASE_URL = 'https://api.kraken.com'
LOGGER = get_kraken_logger(__name__)


class RestClient:

    def __init__(self, key=None, secret=None):
        self.key = key
        self.secret = secret

        headers = {
            'User-Agent': 'aiokraken'
        }
        self.session = aiohttp.ClientSession(headers=headers, raise_for_status=True)

    async def public_request(self, endpoint, data=None):
        """ make public requests to kraken api"""
        LOGGER.info(f'sending request to {BASE_URL}/0/public/{endpoint}')
        LOGGER.info(data)
        async with self.session.post(f'{BASE_URL}/0/public/{endpoint}', json=data) as response:
            if response.status not in (200, 201, 202):
                return {'error': response.status}
            else:
                res = await response.json(encoding='utf-8', content_type=None)
                return res

    async def private_request(self, endpoint, data={}):
        """ make public requests to kraken api"""
        LOGGER.debug(f'sending request to {BASE_URL}/0/private/{endpoint}')
        data['nonce'] = get_nonce()

        url_path = f"/0/private/{endpoint}"
        headers = {
            'API-Key': self.key,
            'API-Sign': self._sign_message(data, url_path)
        }

        async with self.session.post(
                f'{BASE_URL}{url_path}',
                data=data,
                headers=headers) as response:
            if response.status not in (200, 201, 202):
                return {'error': response.status}
            else:
                res = await response.json(encoding='utf-8', content_type=None)
                return res

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

    async def close(self):
        """ Close aiohttp session """
        await self.session.close()

    """ 
         Wrapper methods for private requests : Balance, TradeBalance, OpenOrders, ClosedOrders, QueryOrders, 
         TradesHistory, QueryTrades, OpenPositions, Ledgers, QueryLedgers, TradeVolume, AddExport, ExportStatus,
         RetrieveExport, RemoveExport, AddOrder, CancelOrder, DepositMethods, DepositAddresses, DepositStatus,
         WithdrawInfo, Withdraw, WithdrawStatus, WithdrawCancel
    """
    async def balance(self):
        response = await self.private_request('Balance')
        return response['result']

    async def trade_balance(self, data={}):
        response = await self.private_request('TradeBalance', data)
        return response['result']

    """
        Wrapper methods for public requests :  Time, Assets, AssetPairs, Ticker, OHLC, Depth, Trades, Spread
    """
    async def time(self):
        response = await self.public_request('Time')
        return response['result']

    async def assets(self, data=None):
        response = await self.public_request('Assets', data)
        return response['result']

    async def asset_pairs(self, data=None):
        response = await self.public_request('AssetPairs', data)
        return response['result']
