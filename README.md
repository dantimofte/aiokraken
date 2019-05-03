# aiokraken
Python asyncio client for Kraken REST and Websockets API

## Installation 
    pip install aiokraken

## [REST example](https://github.com/dantimofte/aiokraken/blob/master/aiokraken/examples/rest_example.py)

    from aiokraken import RestClient
    async def get_assets():
        """ get kraken time"""
        rest_kraken = RestClient()

        response = await rest_kraken.assets()
        print(f'response is {response}')

        await rest_kraken.close()
    
    asyncio.get_event_loop().run_until_complete(get_assets())

## [websocket example](https://github.com/dantimofte/aiokraken/blob/master/aiokraken/examples/wss_example.py)

## Documentation

## Compatibility

- python 3.7 and above

## Contributing

Contributions are welcome and i will do my best to merge PR quickly.

Here are some guidelines that makes everything easier for everybody:

1. Fork it.
2. Create a feature branch containing only your fix or feature.
3. Add/Update tests.
4. Create a pull request.

### TODO

- Add wrapper methods for all public and private REST CALLS
- Write tests for the library
- Write documentation for the library

## References

https://www.kraken.com/features/api

## Licence

The MIT License (MIT)
