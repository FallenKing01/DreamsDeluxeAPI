from flask_restx import fields

from extensions import api

userPost = api.model(
    "UserInput",
    {"username": fields.String, "password": fields.String, "role": fields.String},
)

login = api.model("login", {"username": fields.String, "password": fields.String})
