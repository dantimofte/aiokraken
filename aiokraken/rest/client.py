""" AIOKraken rest client """
import urllib
import hashlib
import hmac
import base64
import timeit
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
                res['error'] = "" if 'error' not in res else res['error']
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

        try:
            async with self.session.post(
                    f'{BASE_URL}{url_path}',
                    data=data,
                    headers=headers) as response:
                if response.status not in (200, 201, 202):
                    return {'error': response.status}
                else:
                    res = await response.json(encoding='utf-8', content_type=None)
                    res['error'] = "" if 'error' not in res else res['error']
                    return res
        except aiohttp.ClientResponseError as err:
            LOGGER.error(err)
            return {'error': err}

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
        return response

    async def trade_balance(self, data={}):
        response = await self.private_request('TradeBalance', data)
        if response['error']:
            LOGGER.error(response['error'])
        return response

    async def open_orders(self, data={}):
        response = await self.private_request('OpenOrders', data)
        if response['error']:
            LOGGER.error(response['error'])
        return response

    async def closed_orders(self, data={}):
        response = await self.private_request('ClosedOrders', data)
        if response['error']:
            LOGGER.error(response['error'])
        return response

    async def orders_info(self, data={}):
        response = await self.private_request('QueryOrders', data)
        if response['error']:
            LOGGER.error(response['error'])
        return response

    async def ledgers(self, data={}):
        response = await self.private_request('Ledgers', data)
        if response['error']:
            LOGGER.error(response['error'])
        return response

    async def trade_volume(self, data={}):
        """ Get trade volume and fees info
            https://www.kraken.com/en-us/features/fee-schedule

        """
        response = await self.private_request('TradeVolume', data)
        if response['error']:
            LOGGER.error(response['error'])
        return response

    async def add_order(self, data={}):
        response = await self.private_request('AddOrder', data)
        if response['error']:
            LOGGER.error(response['error'])
        return response

    async def ioc_order(self, data={}):
        """
            This is not a real IOC order but a simulation of one using the following logic:
            1. place a limit order with the lowest expire time accepted by kraken
                expiretm : +5 , this will cancel the order after 5 seconds
            2. as soon as we get a response from kraken with the order id, send a cancel request
            3. get the order and trades information

            !!! Sometimes even if we get a error the order is still placed / canceled
        """

        # step 1: place order
        data['expiretm'] = '+5'
        data['ordertype'] = 'limit'

        start_time = timeit.default_timer()  # measure how much it takes to complete place order + cancel
        LOGGER.info(data)
        order_response = await self.private_request('AddOrder', data)
        if order_response['error']:
            LOGGER.error(order_response['error'])
            return order_response

        # LOGGER.info(add_order_response)
        place_order_time = timeit.default_timer() - start_time
        LOGGER.info(f'place order time : {place_order_time}')

        # step 2: cancel order ASAP
        txid = order_response['result']['txid'][0]
        cancel_response = await self.cancel_order(txid)
        if cancel_response['error']:
            LOGGER.error(cancel_response)
            # maybe i should retry canceling the order

        intermidiary_time = timeit.default_timer() - start_time
        LOGGER.info(f'place order + cancel time : {intermidiary_time}')
        data = {
            "trades": True,
            "txid": txid
        }

        # step 3: get information about what happened
        order_info = await self.orders_info(data)

        final_time = timeit.default_timer() - start_time
        LOGGER.info(f'place order + cancel + get details time : {final_time}')

        return order_info

    async def cancel_order(self, txid):
        """ Cancel open order

        :param txid:
        :return:
        """
        data = {'txid': txid}
        # LOGGER.info(data)
        response = await self.private_request('CancelOrder', data)
        if response['error']:
            LOGGER.error(response['error'])
        return response

    """ Wrapper methods for public requests :  Time, Assets, AssetPairs, Ticker, OHLC, Depth, Trades, Spread """
    async def time(self):
        """ Get server time
            https://www.kraken.com/features/api#get-server-time
            unixtime =  as unix timestamp
            rfc1123 = as RFC 1123 time format
        """
        response = await self.public_request('Time')
        if response['error']:
            LOGGER.error(response['error'])
        return response

    async def assets(self, data=None):
        """ Get asset info
            https://www.kraken.com/features/api#get-asset-info
        """
        response = await self.public_request('Assets', data)
        if response['error']:
            LOGGER.error(response['error'])
        return response

    async def asset_pairs(self, data=None):
        """ Get tradable asset pairs
            https://www.kraken.com/features/api#get-tradable-pairs
        """
        response = await self.public_request('AssetPairs', data)
        if response['error']:
            LOGGER.error(response['error'])
        return response

    async def ticker(self, data={'pair': 'XBTUSD'}):
        """ Get ticker information
            https://www.kraken.com/features/api#get-ticker-info
        """
        response = await self.public_request('Ticker', data)
        if response['error']:
            LOGGER.error(response['error'])
        return response

    async def ohlc(self, data={'pair': 'XBTUSD'}):
        """ Get OHLC data
            https://www.kraken.com/features/api#get-ohlc-data
        """
        response = await self.public_request('OHLC', data)
        if response['error']:
            LOGGER.error(response['error'])
        return response

    async def depth(self, data={'pair': 'XBTUSD'}):
        """ Get OHLC data
            https://www.kraken.com/features/api#get-order-book
        """
        response = await self.public_request('Depth', data)
        if response['error']:
            LOGGER.error(response['error'])
        return response
