from bson import ObjectId
from Utils.Exceptions.customExceptions import CustomException
from Domain.extensions import employersCollection, userCollection
from Controllers.uploadController import deleteImageFromBlob
from Services.EmailSenderService import sendEmail
import bcrypt
from Domain.extensions import salt
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def createEmployeeRepo(employerData):

    user = userCollection.find_one({"_id": ObjectId(employerData["userId"])})

    if user is None:

        raise  CustomException(404, "The user does not exist")

    if userCollection.find_one({"email": employerData["email"]}):

        raise  CustomException(400, "The email is already used")

    hash_pass = hash_password(employerData["password"])

    newEmployer = {

        "name": employerData["name"],
        "email": employerData["email"],
        "password": hash_pass,
        "role": employerData["role"],
        "salary": employerData["salary"],
        "birthdate": employerData["birthdate"],
        "userId": employerData["userId"],
        "description": employerData["description"]
    }

    employersCollection.insert_one(newEmployer)


    newEmployeracc = {

        "email": employerData["email"],
        "password": hash_pass,
        "role": employerData["role"],
        "income": 0,
        "imageUrl": "https://dreamsblob.blob.core.windows.net/profileimages/waiters-concept-illustration_114360-2908.avif",
        "adminId": employerData["userId"],
    }

    userCollection.insert_one(newEmployeracc)
    sendEmail(employerData["name"], "ospatar", employerData["email"])

    return newEmployer

def deleteEmployeeRepo(id):

    employer = employersCollection.find_one({"_id": ObjectId(id)})

    if not employer:
        raise CustomException(404, "Employer not found")

    employerAcc = userCollection.find_one({"email": employer["email"]})

    if employerAcc["imageUrl"] != "https://dreamsblob.blob.core.windows.net/profileimages/waiters-concept-illustration_114360-2908.avif":
        deleteImageFromBlob(employerAcc["imageUrl"], "profileimages")

    employersCollection.delete_one({"_id": ObjectId(id)})
    userCollection.delete_one({"email": employer["email"]})

    return {"Message": "Employer deleted successfully"}, 200

def editEmployeeRepo(data, id, idEmployer):

    employer = employersCollection.find_one({"_id": ObjectId(idEmployer), "userId": id})

    if not employer:
        raise CustomException(404, "Employer not found")

    employer["name"] = data["name"]
    employer["password"] = data["password"]
    employer["role"] = data["role"]
    employer["salary"] = data["salary"]
    employer["description"] = data["description"]
    employer["birthdate"] = data["birthdate"]
    employer["income"] = data["income"]

    employersCollection.update_one({"_id": ObjectId(idEmployer), "userId": id}, {"$set": employer})

def addIncomeRepo(id, income):

    currentEmployer = employersCollection.find_one({"_id": ObjectId(id)})

    if not currentEmployer:
        raise  CustomException(404, "Employer not found")

    employersCollection.update_one({"_id": ObjectId(id)}, {"$inc": {"income": income}})

def getEmployeesByEmailRepo(email):

    currentEmployer = employersCollection.find_one({"email": email})

    if not currentEmployer:
        raise CustomException(404, "Employer not found")

    return currentEmployer

