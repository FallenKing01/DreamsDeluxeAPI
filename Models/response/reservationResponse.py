from flask_restx import fields

from Domain.extensions import api

reservationResponse = api.model(
    "reservationResponse",
    {
        "id": fields.String(attribute="_id"),
        "tableId": fields.String,
        "startTime": fields.DateTime,
        "endTime": fields.DateTime,
        "guests": fields.Integer,
        "specialRequests": fields.String,
    },
)
reservationRestaurantResponse = api.model(
    "restaurantResponse",
    {
        "id": fields.String(attribute="_id"),
        "imageUrl": fields.String,
        "companyName": fields.String,
        "companyAddress": fields.String,
        "companyPhone": fields.String,
        "companyEmail": fields.String,
        "location": fields.String,
    },
)