import os
import asyncio
from aiokraken import RestClient
from aiokraken.utils import get_kraken_logger
from dataclasses import dataclass, field

KEY = os.environ.get('KRAKEN_KEY')
SECRET = os.environ.get('KRAKEN_SECRET')
LOGGER = get_kraken_logger(__name__)


@dataclass
class TickItem:
    """ Handle Kraken tickitem
        data dict :
        a = ask array(<price>, <whole lot volume>, <lot volume>),
        b = bid array(<price>, <whole lot volume>, <lot volume>),
        c = last trade closed array(<price>, <lot volume>),
        v = volume array(<today>, <last 24 hours>),
        p = volume weighted average price array(<today>, <last 24 hours>),
        t = number of trades array(<today>, <last 24 hours>),
        l = low array(<today>, <last 24 hours>),
        h = high array(<today>, <last 24 hours>),
        o = today's opening price
    """
    symbol: str
    data: dict
    bid: float = field(init=False)
    bid_size: float = field(init=False)
    ask: float = field(init=False)
    ask_size: float = field(init=False)
    last_price: float = field(init=False)
    volume: float = field(init=False)
    high: float = field(init=False)
    low: float = field(init=False)
    base_currency: str = field(init=False)
    quote_currency: str = field(init=False)

    def __post_init__(self):
        self.bid = float(self.data['b'][0])
        self.bid_size = float(self.data['b'][2])
        self.ask = float(self.data['a'][0])
        self.ask_size = float(self.data['a'][2])
        self.last_price = float(self.data['c'][0])
        self.volume = float(self.data['v'][1])
        self.high = float(self.data['h'][1])
        self.low = float(self.data['l'][1])
        self.base_currency = self.symbol[1:4]
        self.quote_currency = self.symbol[5:]
        self.data = None


async def get_asset_pairs_v1():
    """
    """
    rest_kraken = RestClient()
    data = {
        "pair": "ADACAD,ADAETH,ADAEUR,ADAUSD,ADAXBT,ATOMCAD,ATOMETH,ATOMEUR,ATOMUSD,ATOMXBT,BCHEUR,BCHUSD,BCHXBT,DASHEUR,DASHUSD,DASHXBT,EOSETH,EOSEUR,EOSUSD,EOSXBT,GNOETH,GNOEUR,GNOUSD,GNOXBT,QTUMCAD,QTUMETH,QTUMEUR,QTUMUSD,QTUMXBT,USDTUSD,ETCETH,ETCXBT,ETCEUR,ETCUSD,ETHXBT,ETHCAD,ETHEUR,ETHGBP,ETHJPY,ETHUSD,LTCXBT,LTCEUR,LTCUSD,MLNETH,MLNXBT,REPETH,REPXBT,REPEUR,REPUSD,XTZCAD,XTZETH,XTZEUR,XTZUSD,XTZXBT,XBTCAD,XBTEUR,XBTGBP,XBTJPY,XBTUSD,XDGXBT,XLMXBT,XLMEUR,XLMUSD,XMRXBT,XMREUR,XMRUSD,XRPXBT,XRPCAD,XRPEUR,XRPJPY,XRPUSD,ZECXBT,ZECEUR,ZECJPY,ZECUSD"
    }
    response = await rest_kraken.ticker(data)
    # print(f'ticker = {response}')
    for ticker_pair, ticker_data in response.items():
        print(f'ticker pair is {ticker_pair}')
        print(f'ticker data is {ticker_data}')
        tick_item = TickItem(ticker_pair, ticker_data)
        print(tick_item)
    await rest_kraken.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(get_asset_pairs_v1())
