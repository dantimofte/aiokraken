import asyncio
import json
import aiohttp
from asyncio import InvalidStateError, CancelledError
from aiokraken.utils import get_kraken_logger

LOGGER = get_kraken_logger(__name__)
SANDBOX_URL = 'wss://ws-sandbox.kraken.com'
PRODUCTION_URL = 'wss://ws.kraken.com'


class WssClient:
    """ asyncio websocket client for kraken """

    def __init__(self):
        self.reqid = 1
        self.pong_futures = {}
        self.connections = {}
        headers = {
            'User-Agent': 'aiokraken'
        }
        self.session = aiohttp.ClientSession(headers=headers, raise_for_status=True)
        asyncio.get_event_loop().create_task(self.clear_expired_pong_futures())

    async def clear_expired_pong_futures(self, futures_cleanup_interval=10):
        await asyncio.sleep(futures_cleanup_interval)
        delete_keys = []
        for future_id, future in self.pong_futures.items():
            try:
                is_complete = any([
                    future.done(),
                    future.cancelled(),
                    future.exception() == TimeoutError
                ])
                if is_complete:
                    delete_keys.append(future_id)
            except (InvalidStateError, CancelledError):
                pass
        for future_id in delete_keys:
            LOGGER.debug(f'clearing expired pong future with id {future_id}')
            del self.pong_futures[future_id]
        asyncio.get_event_loop().create_task(self.clear_expired_pong_futures())

    async def create_connection(self, callback, connection_name="main", connection_env='production'):
        """ Create a new websocket connection """
        websocket_url = PRODUCTION_URL if connection_env == 'production' else SANDBOX_URL

        try:
            async with self.session.ws_connect(websocket_url) as ws:
                self.connections[connection_name] = ws
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = json.loads(msg.data)
                        if isinstance(data, dict) and data['event'] == 'pong' and 'reqid' in data:
                            await self.set_future_pong_value(data)
                        callback(data)
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        LOGGER.error(f'{msg}')
                        LOGGER.error(f'{msg.type}')
                        LOGGER.error(f'{msg.data}')
                        break
                    else:
                        LOGGER.error(f'{msg}')
                        LOGGER.error(f'{msg.type}')
                        LOGGER.error(f'{msg.data}')
                        break
        # in case internet connection fails try and reconnect automatically after 5 seconds
        # there will be no subscriptions though...
        except aiohttp.ClientConnectionError:
            await asyncio.sleep(5)
            asyncio.create_task(
                self.create_connection(callback=callback, connection_name=connection_name, connection_env=connection_env)
            )
            # to resubscribe automatically to all subscriptions i should save them first

    async def close_connection(self, connection_name='main'):
        """ close  websocket connection """
        LOGGER.info('closing the websocket connection')
        resp = await self.connections[connection_name].close()
        del self.connections[connection_name]
        LOGGER.info(f'close response {resp}')

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

    async def kraken_ping(self, connection_name="main", reqid=None, timeout=None):
        """Ping a kraken websocket connection

        Parameters
        ----------
        connection_name : default is main unless otherwise specified
        reqid: will be generated if none specified
        timeout: no timeout unless otherwise specified
        """
        if reqid is None:
            reqid = self.reqid
            self.reqid += 1

        ping_data = {
            'event': 'ping',
            'reqid': reqid
        }

        while connection_name not in self.connections:
            await asyncio.sleep(0.1)
        ws = self.connections[connection_name]

        # Create a new Future object.
        loop = asyncio.get_event_loop()
        future_id = reqid
        self.pong_futures[future_id] = loop.create_future()
        await ws.send_str(json.dumps(ping_data))
        return self.pong_futures[future_id]

    async def set_future_pong_value(self, pong_message):
        """ check if the pong reqid is in the dict of pong_futures created
        """

        future_id = pong_message['reqid']
        if future_id in self.pong_futures:
            self.pong_futures[future_id].set_result(pong_message)
            del self.pong_futures[future_id]
