import marshmallow
from marshmallow import fields, pre_load, post_load

from ..exceptions import AIOKrakenException
from .errors import ErrorsField
from .ohlc import OHLCDataFrameSchema
from .time import TimeSchema
"""A bunch of classes to handle the payload. TOOD : find a better/simpler way ? """


class TimePayloadSchema(marshmallow.Schema):
    class Meta:
        # Pass EXCLUDE as Meta option to keep marshmallow 2 behavior
        # ref: https://marshmallow.readthedocs.io/en/stable/upgrading.html#upgrading-to-3-0
        unknown = getattr(marshmallow, "EXCLUDE", None)

    error = ErrorsField()
    result = fields.Nested(TimeSchema)


class OHLCPayloadSchema(marshmallow.Schema):
    class Meta:
        # Pass EXCLUDE as Meta option to keep marshmallow 2 behavior
        # ref: https://marshmallow.readthedocs.io/en/stable/upgrading.html#upgrading-to-3-0
        unknown = getattr(marshmallow, "EXCLUDE", None)

    error = ErrorsField()
    result = fields.Nested(OHLCDataFrameSchema)
