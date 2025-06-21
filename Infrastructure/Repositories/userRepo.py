
from Domain.extensions import  userCollection,employersCollection
from bson import ObjectId
from Utils.Exceptions.customExceptions import CustomException
from Infrastructure.Repositories.tablesMapRepo import createTableMapRepo
from Services.EmailSenderService import sendEmail
import bcrypt
from Domain.extensions import salt
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def createUserRepo(newUser):

    user = userCollection.find_one({"email": newUser["username"]})

    if user:

        raise CustomException(409, "User with this email already exists")

    hashed_password = hash_password(newUser["password"])

    user = {

        "email": newUser["username"],
        "password": hashed_password,
        "role": "admin",
        "totalAmount": 0,
        "companyName": newUser["companyName"],
        "companyAddress": newUser["companyAddress"],
        "companyPhone": newUser["companyPhone"],
        "location": newUser["location"],
        "county": newUser["county"],
        "totalRecensions": 0,
        "totalRatings": [],
        "finalRating": 0
    }

    insertedItm = userCollection.insert_one(user)
    insertedId = str(insertedItm.inserted_id)

    if user["role"] == "admin":

        createTableMapRepo(insertedId)

    sendEmail(newUser["companyName"], "admin", newUser["username"])

    return insertedId

def verifyUserRepo(email):

    user = userCollection.find_one({"email": email})

    if user is not None:

        raise CustomException(409,"User with this email already exists")

def getUserByIdRepo(id):

    if len(id) == 24 and all(c in "0123456789abcdefABCDEF" for c in id):

        user = userCollection.find_one({"_id": ObjectId(id)})

        if user is None:

            raise CustomException(404, "User not found")

        return user

    else:

        raise CustomException(400, "Invalid user ID")

def getUserByEmailRepo(email):

    user = userCollection.find_one({"email": email})

    if user is None:

        raise CustomException(404, "User not found")

    user["_id"] = str(user["_id"])

    return user

def deleteUserById(id):

    objId = ObjectId(id)

    user = userCollection.find_one({"_id": objId})

    if user is None:
        raise CustomException(404, "User not found")

    userCollection.delete_one({"_id": objId})

def getUserAdminRepo(id):

    if len(id) == 24 and all(c in "0123456789abcdefABCDEF" for c in id):

        user = userCollection.find_one({"_id": ObjectId(id)})

        if user is None:
            raise CustomException(404, "User not found")

        admin = employersCollection.find_one({'email': user["email"]})

        if admin is None:

            raise CustomException(404, "Admin not found")

        return {"id": admin["userId"]}

    else:

        raise CustomException(400, "Invalid user ID")
