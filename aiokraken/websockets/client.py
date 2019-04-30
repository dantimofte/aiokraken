import asyncio
import json
import aiohttp
from aiokraken.utils import get_kraken_logger

LOGGER = get_kraken_logger(__name__)
SANDBOX_URL = 'wss://ws-sandbox.kraken.com'
PRODUCTION_URL = 'wss://ws.kraken.com'


class WssClient:
    """ asyncio websocket client for kraken """

    def __init__(self):
        self.connections = {}
        headers = {
            'User-Agent': 'aiokraken'
        }
        self.session = aiohttp.ClientSession(headers=headers, raise_for_status=True)

    async def create_connection(self, callback, connection_name="main", connection_env='production'):
        """ Create a new websocket connection """
        websocket_url = PRODUCTION_URL if connection_env == 'production' else SANDBOX_URL

        async with self.session.ws_connect(websocket_url) as ws:
            self.connections[connection_name] = ws
            async for msg in ws:
                data = json.loads(msg.data)
                callback(data)

    async def subscribe(self, pairs, subscription, connection_name="main"):
        """ add new subscription """
        while connection_name not in self.connections:
            await asyncio.sleep(0.1)
        ws = self.connections[connection_name]
        subscription_data = {
            "event": "subscribe",
            "pair": pairs,
            "subscription": subscription
        }
        await ws.send_str(json.dumps(subscription_data))
