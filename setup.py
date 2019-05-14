from setuptools import setup, find_packages

setup(
    name='aiokraken',
    version='1.1.0',
    description='Python client library for the Kraken Rest and Websocket API using asyncio and aiohttp',
    author='Dan Timofte',
    author_email='dan@arcane.no',
    url='https://github.com/dantimofte/aiokraken',
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "aiodns",
        "cchardet"
    ],
)
