from setuptools import setup

setup(
    name='aiokraken',
    version='1.0.1',
    description='Python client library for the Kraken Rest and Websocket API using asyncio and aiohttp',
    author='Dan Timofte',
    author_email='dan@arcane.no',
    url='https://github.com/dantimofte/aiokraken',
    packages=['aiokraken'],
    install_requires=[
        "aiohttp",
        "aiodns",
        "cchardet"
    ],
)
