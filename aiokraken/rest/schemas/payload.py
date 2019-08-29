import marshmallow
from marshmallow import fields, pre_load, post_load

from ..exceptions import AIOKrakenException


class PayloadSchema(marshmallow.Schema):
    class Meta:
        # Pass EXCLUDE as Meta option to keep marshmallow 2 behavior
        # ref: https://marshmallow.readthedocs.io/en/3.0/upgrading.html
        unknown = getattr(marshmallow, "EXCLUDE", None)


    @pre_load(pass_many=True)
    def check_errors(self, data, many, **kwargs):
        # TODO : usual schema to manage error parsing
        if "error" not in data: # TMP
            raise marshmallow.ValidationError("error field not found")

        if len(data.get("error")) > 0:  # TODO : currently buggy on error (silent retry ?). TOFIX
            raise AIOKrakenException("ERROR in message from server: " + "\n".join(data.get("error")))
            # TODO : check for errors and raise appropriate exception !
        return data['result']
