from marshmallow import Schema, fields, validate


class DimensionSchema(Schema):
    key = fields.String()
    val = fields.String()

class MetricSchema(Schema):
    key = fields.String()
    val = fields.Integer()

class InsertSchema(Schema):
    dim = fields.List(
        fields.Nested(
            DimensionSchema()
        ),
        validate=validate.Length(min=1),
        required=True
    )
    metrics = fields.List(
        fields.Nested(
            MetricSchema()
        ),
        validate=validate.Length(min=1)
    )

class SearchSchema(Schema):
    dim = fields.List(
        fields.Nested(
            DimensionSchema()
        ),
        validate=validate.Length(min=1)
    )

