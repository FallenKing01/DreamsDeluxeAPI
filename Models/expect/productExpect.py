from flask_restx import fields

from Domain.extensions import api

productPost = api.model(
    "Product",
    {
        "name": fields.String(required=True),
        "price": fields.Float(required=True),
        "qty": fields.Integer(required=True),
        "table_id": fields.String(required=True, attribute="_id"),
    },
)

productPostAdmin = api.model(
    "addMenuProduct",
    {
        "name": fields.String(required=True),
        "type": fields.String(required=True),
        "price": fields.Float(required=True),       
    },
)
