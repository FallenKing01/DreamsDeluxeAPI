from flask_restx import fields

from extensions import api

userPost = api.model(
    "UserInput",
    {
    "username": fields.String, 
    "password": fields.String, 
    "role": fields.String,
    "companyName": fields.String,
    "companyAddress": fields.String,
    "companyPhone": fields.String,
    "companyEmail": fields.String,
    "location": fields.String,

    },
)

login = api.model("login", {"username": fields.String, "password": fields.String})
