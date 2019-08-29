import marshmallow
from marshmallow import fields, pre_load, post_load


from ..exceptions import AIOKrakenException
from ...model.time import Time


class TimeSchema(marshmallow.Schema):
    class Meta:
        # Pass EXCLUDE as Meta option to keep marshmallow 2 behavior
        # ref: https://marshmallow.readthedocs.io/en/stable/upgrading.html#upgrading-to-3-0
        unknown = getattr(marshmallow, "EXCLUDE", None)

    """ Schema to parse the string received"""
    unixtime = marshmallow.fields.Int(required=True)
    # rfc1123 ??

    @marshmallow.post_load(pass_many=False)
    def make_time(self, data, **kwargs):
        return Time(data.get("unixtime"))

