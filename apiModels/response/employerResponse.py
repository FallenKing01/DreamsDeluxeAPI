from flask_restx import fields

from extensions import api

employerResponse = api.model("Employer Post", {

    "id": fields.String(attribute="_id"),
    "name": fields.String,
    "email": fields.String,
    "password": fields.String,
    "role": fields.String,
    "salary": fields.Float,
    "birthdate": fields.String,
    "userId": fields.String

})
