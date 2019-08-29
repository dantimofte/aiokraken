import marshmallow

class SchemaBase(marshmallow.Schema):
    class Meta:
        # Pass EXCLUDE as Meta option to keep marshmallow 2 behavior
        # ref: https://marshmallow.readthedocs.io/en/3.0/upgrading.html
        unknown = getattr(marshmallow, "EXCLUDE", None)


class TimeSchema(SchemaBase):
    """ Schema to parse the string received"""
    unixtime = marshmallow.fields.Int(required=True)
    # rfc1123 ??

    # @marshmallow.post_load(pass_many=False)
    # def make_time(self, data, **kwargs):
    #     return Time(data.get("unixtime"))


# == Schemas == #
# TODO : reuse this for other kind of payload data ?
class TimePayloadSchema(marshmallow.Schema):
    error = marshmallow.fields.List(marshmallow.fields.Str())
    result = marshmallow.fields.Nested(TimeSchema)

    @marshmallow.post_load(pass_many=False)
    def filter_error(self, data, **kwargs):
        if len(data.get("error")) > 0: # TODO : currently buggy on error (silent retry ?). TOFIX
            raise BokenException("ERROR in message from server: " + data.get("error"))
        else:
            # just get the result
            return data.get("result")


