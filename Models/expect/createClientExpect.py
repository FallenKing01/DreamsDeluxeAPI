from flask_restx import fields

from Domain.extensions import api

clientPost = api.model(
    "Client post",
    {   "clientName": fields.String,
        "username": fields.String,
        "password": fields.String,
        "location": fields.String,
        "county": fields.String,
        "phoneNumber": fields.String,
    },
)

getRestaurantsExpect = api.model(
    "Get restaurants",
    {
        "county": fields.String,
        "location": fields.String,
    },
)