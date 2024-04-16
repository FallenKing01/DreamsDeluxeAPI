from Utils.Exceptions.customExceptions import CustomException
from Domain.extensions import employersCollection, userCollection
from datetime import datetime, timedelta

from flask_jwt_extended import create_access_token



def loginRepo(accountData):

        username = accountData["username"]
        password = accountData["password"]

        user = userCollection.find_one({"email": username})

        if user is None:
            raise CustomException(404, "User not found")

        if password != user.get("password"):
            raise CustomException(401, "Wrong password")

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