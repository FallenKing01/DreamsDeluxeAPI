from Services.EmailSenderService import sendResetPasswordEmail, sendPasswordResetConfirmationEmail
from Utils.Exceptions.customExceptions import CustomException
from Domain.extensions import employersCollection, userCollection
from datetime import datetime, timedelta

from flask_jwt_extended import create_access_token
import random



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

def forgotPasswordRepo(email):

        user = userCollection.find_one({"email": email})

        if user is None:

            raise CustomException(404, "User not found")

        generatedNumber = random.randint(1000, 9999)
        userData = {
            "id": str(user["_id"]),
            "name": user.get("name"),
            "email": email,
            "code": generatedNumber,
        }

        userCollection.update_one({"email": email}, {"$set": {"code": generatedNumber}})

        sendResetPasswordEmail(userData["name"], userData["email"], userData["code"])

        return {"message": create_access_token(userData,additional_claims=userData,expires_delta=timedelta(minutes=30))}, 201



def resetPasswordRepo(email,password,code):

        user = userCollection.find_one({"email": email})
        if user is None:

            raise CustomException(404, "User not found")


        if code != user.get("code"):

            raise CustomException(401, "Wrong code")

        userData = {
            "id": str(user["_id"]),
            "name": user.get("name"),
            "email": email,
        }

        sendPasswordResetConfirmationEmail(userData["email"])
        userCollection.update_one({"email": email}, {"$set": {"password": password}})

        return {"message": "Password reset successful"}, 201






