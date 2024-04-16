from flask_restx import fields

from Models.response.productResponse import productTable
from Domain.extensions import api

tablePostResponse = api.model(
    "Tabel",
    {
        "id": fields.String(attribute="_id"),
        "name": fields.String,
        "capacity": fields.Integer,
        "billValue": fields.Float,
        "userId": fields.String,  # If you want to include user_id as well
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
