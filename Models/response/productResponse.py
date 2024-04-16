from flask_restx import fields

from Domain.extensions import api

productTable = api.model(
    "TableProduct",
    {
        "id": fields.String,
        "name": fields.String,
        "price": fields.Float,
        "qty": fields.Integer,
    },
)



tableget = api.model(
    "getById",
    {
        "id": fields.String(attribute="_id"),
        "name": fields.String,
        "capacity": fields.Integer,
        "billValue": fields.Float,
        "products": fields.Nested(productTable),
    },
)

productAdd =api.model(
    "ProductAddResponse",
    {
        "id": fields.String(attribute="_id"),
        "name": fields.String,
        "price": fields.Float,
        "qty": fields.Integer,
    },
)

productAddAdmin =api.model(
    "ProductAddResponseAdmin",
    {
        "id": fields.String(attribute="_id"),
        "name": fields.String,
        "type": fields.String(required=True),
        "price": fields.Float,
    },
)