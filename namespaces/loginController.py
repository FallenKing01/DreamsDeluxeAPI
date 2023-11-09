from datetime import datetime, timedelta

from flask import abort
from flask_jwt_extended import create_access_token
from flask_restx import Namespace, Resource

from apiModels.expect.userExpect import login
from extensions import db

nsLogin = Namespace("login", description="Login user")
collection = db["user"]


@nsLogin.route("/")
class LoginApi(Resource):
    @nsLogin.expect(login)
    def post(self):
        username = nsLogin.payload.get("username")
        password = nsLogin.payload.get("password")

        user = collection.find_one({"email": username})

        if user is None:
            abort(404, "User not found")

        if password != user.get("password"):
            abort(401, "Wrong password")

        userData = {
            "id": str(user["_id"]),
            "username": user.get("email"),
            "role": user.get("role"),
        }
        expires = datetime.utcnow() + timedelta(days=30)
        return {
            "Authentication successful": create_access_token(
                userData,
                additional_claims=userData,
                expires_delta=expires - datetime.utcnow(),
            )
        }, 201
