from marshmallow import Schema, fields, validate


class DimensionSchema(Schema):
    key = fields.String(required=True)
    val = fields.String(required=True)


class MetricSchema(Schema):
    key = fields.String(required=True)
    val = fields.Integer(required=True)


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
        validate=validate.Length(min=1),
        required=True
    )


class SearchSchema(Schema):
    dim = fields.List(
        fields.Nested(
            DimensionSchema()
        ),
        validate=validate.Length(min=1)
    )
