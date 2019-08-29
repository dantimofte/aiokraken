from marshmallow import fields


class ErrorsField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return value.title()

    def _deserialize(self, value, attr, data, **kwargs):
        return value.lower()