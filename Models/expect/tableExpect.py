from flask_restx import fields

from Domain.extensions import api

tablePost = api.model(
    "TabelExpect",
    {
        "name": fields.String,
        "capacity": fields.Integer,
    },
)
