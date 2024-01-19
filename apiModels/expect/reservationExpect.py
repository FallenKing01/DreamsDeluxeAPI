from flask_restx import fields

from extensions import api


reservationExpect = api.model(
    "reservationExpect",
    {
        "reservationName": fields.String,
        "startTime": fields.DateTime,
        "endTime": fields.DateTime,
        "guests": fields.Integer,
        "specialRequests": fields.String,
    },
)
