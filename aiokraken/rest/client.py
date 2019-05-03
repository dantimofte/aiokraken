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
        LOGGER.debug(f'sending request to {BASE_URL}/0/public/{endpoint}')
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
        if response['error']:
            LOGGER.error(response['error'])
            return {}
        return response['result']

    async def trade_balance(self, data={}):
        response = await self.private_request('TradeBalance', data)
        if response['error']:
            LOGGER.error(response['error'])
            return {}
        return response['result']

    async def ledgers(self, data={}):
        response = await self.private_request('Ledgers', data)
        if response['error']:
            LOGGER.error(response['error'])
            return {}
        return response['result']

    async def trade_volume(self, data={}):
        """ Get trade volume and fees info
            https://www.kraken.com/en-us/features/fee-schedule

        """
        response = await self.private_request('TradeVolume', data)
        if response['error']:
            LOGGER.error(response['error'])
            return {}

        return response['result']

    """ Wrapper methods for public requests :  Time, Assets, AssetPairs, Ticker, OHLC, Depth, Trades, Spread """
    async def time(self):
        """ Get server time
            unixtime =  as unix timestamp
            rfc1123 = as RFC 1123 time format
        """
        response = await self.public_request('Time')
        if response['error']:
            LOGGER.error(response['error'])
            return {}
        return response['result']

    async def assets(self, data=None):
        """ Get asset info"""
        response = await self.public_request('Assets', data)
        if response['error']:
            LOGGER.error(response['error'])
            return {}
        return response['result']

    async def asset_pairs(self, data=None):
        """ Get tradable asset pairs """
        response = await self.public_request('AssetPairs', data)
        if response['error']:
            LOGGER.error(response['error'])
            return {}
        return response['result']

    async def ticker(self, data={'pair': 'XBTUSD'}):
        """ Get ticker information """
        response = await self.public_request('Ticker', data)
        if response['error']:
            LOGGER.error(response['error'])
            return {}
        return response['result']
