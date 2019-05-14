
import asyncio
import signal
from aiokraken import WssClient


def process_message(message):
    print(f'processed message {message}')


async def main() -> None:
    """Start kraken websockets api
    """
    wss_kraken = WssClient()

    asyncio.ensure_future(
        wss_kraken.create_connection(process_message)
    )
    await wss_kraken.subscribe(
        ['XBT/USD'],
        {
            "name": 'ticker'
        }
    )
    await wss_kraken.subscribe(
        ['ETH/USD'],
        {
            "name": '*'
        }
    )


@asyncio.coroutine
def ask_exit(sig_name):
    print("got signal %s: exit" % sig_name)
    yield from asyncio.sleep(2.0)
    asyncio.get_event_loop().stop()


loop = asyncio.get_event_loop()

loop.create_task(
    main()
)
for signame in ('SIGINT', 'SIGTERM'):
    loop.add_signal_handler(
        getattr(signal, signame),
        lambda: asyncio.ensure_future(ask_exit(signame))
    )
loop.run_forever()
