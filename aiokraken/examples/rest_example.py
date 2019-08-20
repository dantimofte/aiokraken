import os
import asyncio
import signal
from aiokraken import RestClient
from aiokraken.utils import get_kraken_logger

from aiokraken.rest import krak_key
KEY = krak_key.key
SECRET = krak_key.secret
LOGGER = get_kraken_logger(__name__)


# PRIVATE REQUEST EXAMPLES
async def get_balance():
    """Start kraken websockets api
    """
    rest_kraken = RestClient(KEY, SECRET)
    response = await rest_kraken.balance()
    await rest_kraken.close()
    print(f'response is {response}')


async def get_trade_balance():
    """ get account trade balance
    """
    rest_kraken = RestClient(KEY, SECRET)
    data = {
        'asset': 'XXBT'
    }
    response = await rest_kraken.trade_balance(data)
    print(f'response is {response}')
    response = await rest_kraken.trade_balance()
    print(f'response is {response}')
    await rest_kraken.close()


async def get_trade_volume():
    """ get account trade volume
    """
    rest_kraken = RestClient(KEY, SECRET)

    data = {
        'pair': 'all'
    }
    response = await rest_kraken.trade_volume(data)
    print(f'response is {response}')
    response = await rest_kraken.trade_volume()
    print(f'response is {response}')
    await rest_kraken.close()


async def get_ledgers():
    """
    """
    rest_kraken = RestClient(KEY, SECRET)

    response = await rest_kraken.ledgers()
    print(f'response is {response}')
    await rest_kraken.close()


async def get_ledgers():
    """
    """
    rest_kraken = RestClient(KEY, SECRET)

    response = await rest_kraken.ledgers()
    print(f'response is {response}')
    await rest_kraken.close()


async def get_open_orders():
    """
    """
    rest_kraken = RestClient(KEY, SECRET)
    response = await rest_kraken.open_orders()
    open_orders = response['open']
    for key, order in open_orders.items():
        LOGGER.info(f'{key} : {order}')
    # from pprint import pprint
    # pprint(response)
    # for key, value in response:
    #     LOGGER.info(f'{key} : {value}')
    await rest_kraken.close()


async def get_closed_orders():
    """
    """
    rest_kraken = RestClient(KEY, SECRET)
    response = await rest_kraken.closed_orders()
    LOGGER.info(response)
    await rest_kraken.close()


async def get_orders_info():
    """
    """
    rest_kraken = RestClient(KEY, SECRET)
    response = await rest_kraken.orders_info()
    LOGGER.info(response)
    await rest_kraken.close()


async def add_order():
    """

    :return:
    """

    data = {
        "pair": "XDGXBT",
        "type": "sell",
        "ordertype": "limit",
        "price": "0.0000013",
        "volume": "7900",
        # "timeInForce": 'IOC',
        # "expiretm": "+5",
        "validate": True
    }
    rest_kraken = RestClient(KEY, SECRET)
    response = await rest_kraken.add_order(data)
    LOGGER.info(response)
    await rest_kraken.close()


async def place_ioc_order():
    """
    """
    data = {
        "pair": "XDGXBT",
        "type": "sell",
        "price": "0.00001729",
        "volume": "7900"
    }
    rest_kraken = RestClient(KEY, SECRET)
    response = await rest_kraken.ioc_order(data)
    LOGGER.info(response)
    await rest_kraken.close()


async def test_ioc_order():
    """
     Buy maximum amount of doge with BTC available using a ioc type of order
    :return:
    """
    rest_kraken = RestClient(KEY, SECRET)
    balance = await rest_kraken.balance()
    btc_balance = float(balance['result']['XXBT'])
    LOGGER.info(f'btc balance is {btc_balance}')

    ticker = await rest_kraken.ticker(data={'pair': 'XDGXBT'})
    doge_price = ticker['result']['XXDGXXBT']['a'][0]
    LOGGER.info(f'doge ask price : {doge_price}')

    fees_result = await rest_kraken.trade_volume({'pair': 'XDGXBT'})
    fee_doge = fees_result['result']['fees']['XXDGXXBT']['fee']
    fee_doge = float(fee_doge) / 100
    LOGGER.info(f'doge take fee is {fee_doge}')
    fee_to_pay = btc_balance * fee_doge
    LOGGER.info(f'fee to pay : {fee_to_pay}')

    volume_to_buy = btc_balance / float(doge_price)
    LOGGER.info(f'can buy {int(volume_to_buy)} doge without fee')

    btc_left = btc_balance / (1 + float(fee_doge))
    LOGGER.info(f'btc_left : {btc_left}')
    volume_to_buy = btc_left / float(doge_price)
    LOGGER.info(f'can buy {int(volume_to_buy)} doge with fee subtracted')

    data = {
        "pair": "XDGXBT",
        "type": "buy",
        "price": doge_price,
        "volume": int(volume_to_buy)
    }

    ioc_response = await rest_kraken.ioc_order(data)
    LOGGER.info(f'ioc response is {ioc_response}')

    await rest_kraken.close()


async def cancel_order(txid):
    """

    :return:
    """

    rest_kraken = RestClient(KEY, SECRET)
    response = await rest_kraken.cancel_order(txid)
    LOGGER.info(response)
    await rest_kraken.close()


# PUBLIC REQUEST EXAMPLES
async def get_time():
    """ get kraken time"""
    rest_kraken = RestClient()
    response = await rest_kraken.time()
    await rest_kraken.close()
    print(f'response is {response}')


async def get_assets():
    """ get kraken time"""
    rest_kraken = RestClient()

    # with options
    data = {
        "asset": "ADA,ETH"
    }
    response = await rest_kraken.assets(data)
    print(f'response is {response}')

    # no options
    response = await rest_kraken.assets()
    print(f'response is {response}')

    await rest_kraken.close()


async def get_asset_pairs_v1():
    """
        Make request using public_request method
        Allows more freedom than using the wrapper methods
    """
    rest_kraken = RestClient()
    data = {
        "info": "fees",
        "pair": "ADACAD"
    }
    response = await rest_kraken.public_request('AssetPairs', data=data)
    print(f'response is {response}')
    await rest_kraken.close()


async def get_asset_pairs_v2():
    """ Get asset pairs using the wrapper method
    """
    rest_kraken = RestClient()
    data = {
        "info": "fees",
        "pair": "ADACAD, ADAEUR"
    }

    response = await rest_kraken.asset_pairs(data)
    print(f'response is {response}')
    await rest_kraken.close()


async def get_ohlc():
    """ Get asset pairs using the wrapper method
    """
    rest_kraken = RestClient()
    data = {
        "pair": "ADACAD",
        "interval": 240
    }

    response = await rest_kraken.ohlc(data)
    print(f'response is {response}')
    await rest_kraken.close()


async def get_depth():
    """ Get asset pairs using the wrapper method
    """
    rest_kraken = RestClient()
    data = {
        "pair": "ADACAD",
        "count": 500  # this appers to be the maximum accepted value
    }

    response = await rest_kraken.depth(data)
    print(f'response is {response}')
    await rest_kraken.close()


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
# loop.create_task(
#     get_balance()
# )
# loop.run_forever()

# loop.run_until_complete(get_time())
# loop.run_until_complete(get_assets())
# loop.run_until_complete(get_asset_pairs_v1())
# loop.run_until_complete(get_asset_pairs_v2())
loop.run_until_complete(get_balance())
# loop.run_until_complete(get_trade_balance())
# loop.run_until_complete(get_trade_volume())
# loop.run_until_complete(get_ledgers())
# loop.run_until_complete(get_ohlc())
# loop.run_until_complete(get_depth())
# loop.run_until_complete(get_orders_info())
# loop.run_until_complete(get_open_orders())
# loop.run_until_complete(cancel_order('OLCXWY-UU6CW-PUSPSH'))
# loop.run_until_complete(add_order())
# loop.run_until_complete(place_ioc_order())
# loop.run_until_complete(test_strategy())


