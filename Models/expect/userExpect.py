from flask_restx import fields

from Domain.extensions import api

userPost = api.model(
    "UserInput",
    {
    "username": fields.String, 
    "password": fields.String, 
    "companyName": fields.String,
    "companyAddress": fields.String,
    "companyPhone": fields.String,
    "location": fields.String,
    "county": fields.String,
    },
)

login = api.model("login", {"username": fields.String, "password": fields.String})
