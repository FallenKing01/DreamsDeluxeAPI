from flask_restx import fields

from extensions import api

getUserId = api.model(
    "User", {"email": fields.String, "password": fields.String, "role": fields.String}
)

getUserEmail = api.model(
    "User",
    {
        "id": fields.String(attribute="_id"),
        "password": fields.String,
        "role": fields.String,
        "totalAmount": fields.Float,
    },
)

getUsers = api.model(
    "Users",
    {
        "id": fields.String(attribute="_id"),
        "email": fields.String,
        "password": fields.String,
        "role": fields.String,
        "imageUrl": fields.String,
    },
)
getUserAdmin = api.model(
    "Users",
    {
        "id": fields.String,
    },
)