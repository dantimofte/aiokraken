import time
import unittest
from parameterized import parameterized
import json
import marshmallow
"""
Test module.
This is intended for extensive testing, using parameterized, hypothesis or similar generation methods
For simple usecase examples, we should rely on doctests.
"""

class TestTimeSchema(unittest.TestCase):

    def setUp(self) -> None:
        self.schema = schemas.TimeSchema()

    @parameterized.expand([
        # we make sure we are using a proper json string
        [json.dumps({"unixtime": 11111111})],
    ])
    def test_load_ok(self, payload):
        """ Verifying that expected data parses properly """
        parsed = self.schema.loads(payload)
        assert isinstance(parsed, Time)

    @parameterized.expand([
        # we make sure we are using a proper json string
        [json.dumps({"what": "isit"})],
        [json.dumps({"unixtime": "some_string"})],
    ])
    def test_load_fail(self, payload):
        """ Verifying that unexpected data fails properly """
        with self.assertRaises(marshmallow.exceptions.ValidationError):
            self.schema.loads(payload)




class TestTimePayloadSchema(unittest.TestCase):

    def setUp(self) -> None:
        self.schema = schemas.TimePayloadSchema()

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
        [json.dumps({"error": "some_string", "result": "something else"})],
    ])
    def test_load_fail(self, payload):
        """ Verifying that unexpected data fails properly """
        with self.assertRaises(marshmallow.exceptions.ValidationError):
            self.schema.loads(payload)



