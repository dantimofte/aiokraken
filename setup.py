from setuptools import setup

setup(
    name='aiokraken',
    version='1.0.0',
    description='backend app',
    author='Dan Timofte',
    author_email='dan@arcane.no',
    url='arcane.no',
    packages=['aiokraken'],
    install_requires=[
        "aiohttp",
        "aiodns",
        "cchardet"
    ],
)
