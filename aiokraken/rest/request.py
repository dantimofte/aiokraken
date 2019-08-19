
from dataclasses import dataclass, asdict, field

import typing

"""
A dataclass representing a request
"""


@dataclass(frozen=True)
class Request:
    """
    Request : one use only -> immutable
    Idempotent call (or 'retry' semantic ? based on error code ?)
    """

    url: str = ""
    data: typing.Dict = field(default_factory=dict)
    headers: typing.Dict = field(default_factory=dict)

    async def __call__(self, response):
        """
        Locally modelling the request.
        returning possible responses, and how to deal with them
        :return:
        """

        if response.status not in (200, 201, 202):
            return {
                'request': asdict(self),
                'error': response.status}
        else:
            res = await response.json(encoding='utf-8', content_type=None)
            res['request'] = asdict(self),
            res['error'] = "" if 'error' not in res else res['error']
            return res
