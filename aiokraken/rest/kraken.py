from dataclasses import dataclass

import typing


@dataclass
class Response:
    """
    Representing expected response
    """

    status: int



def resource(name):

    def decorator(fun):

        def wrapper(*args, **kwargs):
            response = fun(*args, **kwargs)

        return wrapper
    return decorator





@resource('Time')
def time():
    return {'unixtime': typing.SupportsInt, 'rfc1123': typing.AnyStr}
    # Note: These are schemas ?? see marshmallow...

#@headers # TODO : define specific headers
@resource('Balance')
def balance():
    return {}