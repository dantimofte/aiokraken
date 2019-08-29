import marshmallow
from marshmallow import fields, pre_load, post_load

from .payload import PayloadSchema
from ..exceptions import AIOKrakenException
from ...model.time import Time


class TimeSchema(PayloadSchema):
    """ Schema to parse the string received"""
    unixtime = marshmallow.fields.Int(required=True)
    # rfc1123 ??

    @marshmallow.post_load(pass_many=False)
    def make_time(self, data, **kwargs):
        return Time(data.get("unixtime"))

