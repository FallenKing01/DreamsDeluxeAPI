
from Domain.extensions import  userCollection,employersCollection
from bson import ObjectId
from Utils.Exceptions.customExceptions import CustomException
def createUserRepo(newUser):

    user = userCollection.find_one({"email": newUser["username"]})

    if user:
        raise CustomException(409, "User with this email already exists")

    # Create a new user

    user = {
        "email": newUser["username"],
        "password": newUser["password"],
        "role": newUser["role"],
        "totalAmount": 0,
        "companyName": newUser["companyName"],
        "companyAddress": newUser["companyAddress"],
        "companyPhone": newUser["companyPhone"],
        "companyEmail": newUser["companyEmail"],
        "location": newUser["location"],
        "imageUrl": "https://dreamsblob.blob.core.windows.net/profileimages/d9e0d9f0-d02c-4bce-9f14-82464104f74b"
    }

    insertedItm = userCollection.insert_one(user)

    insertedId = str(insertedItm.inserted_id)

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
