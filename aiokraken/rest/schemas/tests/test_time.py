import time
import unittest
from parameterized import parameterized
import json
import marshmallow

from ..time import TimeSchema
from ...exceptions import AIOKrakenException

"""
Test module.
This is intended for extensive testing, using parameterized, hypothesis or similar generation methods
For simple usecase examples, we should rely on doctests.
"""


class TestTimeSchema(unittest.TestCase):

    def setUp(self) -> None:
        self.schema = TimeSchema()

    @parameterized.expand([
        # we make sure we are using a proper json string
        [json.dumps({'error': [], 'result':{"unixtime": 11111111}})],
    ])
    def test_load_ok(self, payload):
        """ Verifying that expected data parses properly """
        parsed = self.schema.loads(payload)

    @parameterized.expand([
        # we make sure we are using a proper json string
        [json.dumps({"what": "isit"})],
        [json.dumps({"error": ["some_string"], "result": "something else"})],
    ])
    def test_load_fail(self, payload):
        """ Verifying that unexpected data fails properly """
        with self.assertRaises((AIOKrakenException, marshmallow.exceptions.ValidationError)):
            self.schema.loads(payload)



