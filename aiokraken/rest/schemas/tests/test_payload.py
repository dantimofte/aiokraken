import time
import unittest
from parameterized import parameterized
import json
import marshmallow

from ..payload import PayloadSchema
from ...exceptions import AIOKrakenException


class TestTimePayloadSchema(unittest.TestCase):

    def setUp(self) -> None:
        self.schema = PayloadSchema()

    @parameterized.expand([
        # we make sure we are using a proper json string
        [json.dumps({'error': [], 'result':{'answer': 42}})],
    ])
    def test_load_result(self, payload):
        """ Verifying that expected data parses properly """
        parsed = self.schema.loads(payload)
        assert parsed == {'answer': 42}

    @parameterized.expand([
        # we make sure we are using a proper json string
        [json.dumps({'error': ['BOUH'], 'result':42})],
    ])
    def test_load_error(self, payload):
        """ Verifying that expected data parses properly """
        with self.assertRaises(AIOKrakenException):
            self.schema.loads(payload)

    @parameterized.expand([
        # we make sure we are using a proper json string
        [json.dumps({"what": "isit"})],
    ])
    def test_load_fail(self, payload):
        """ Verifying that unexpected data fails properly """
        with self.assertRaises(marshmallow.exceptions.ValidationError):
            self.schema.loads(payload)
