import os
import asyncio
import signal
from aiokraken import RestClient
from aiokraken.utils import get_kraken_logger


KEY = os.environ.get('KRAKEN_KEY')
SECRET = os.environ.get('KRAKEN_SECRET')
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
    """ get account trade volume
    """
    rest_kraken = RestClient(KEY, SECRET)

    data = {
        'pair': 'ADAEUR,ADACAD',
        'fee-info': 'false'
    }
    response = await rest_kraken.ledgers()
    print(f'response is {response}')
    response = await rest_kraken.ledgers(data)
    print(f'response is {response}')
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
# loop.run_until_complete(get_trade_balance())
loop.run_until_complete(get_trade_volume())
# loop.run_until_complete(get_ledgers())

