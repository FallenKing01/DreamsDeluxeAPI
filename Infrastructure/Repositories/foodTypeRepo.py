from Domain.extensions import foodTypeCollection,userCollection
from Utils.Exceptions.customExceptions import CustomException
from bson import ObjectId

def createFoodTypeRepo(foodType):


    if userCollection.find_one({"_id": ObjectId(foodType["adminId"])}) is None:

        raise CustomException(404, "Admin not found")


    insertedType = foodTypeCollection.insert_one(foodType)

    response = {
        "name" : foodType["typeName"],
        "adminId" : foodType["adminId"],
        "id" : str(insertedType.inserted_id)
    }

    return response

def getFoodTypesRepo(adminId):

    if userCollection.find_one({"_id": ObjectId(adminId)}) is None:

        raise CustomException(404, "Admin not found")

    foodTypes = foodTypeCollection.find({"adminId": adminId})

    foodTypesList = []

    for foodType in foodTypes:

        foodType['_id'] = str(foodType['_id'])

        if 'adminId' in foodType:

            foodType['adminId'] = str(foodType['adminId'])

        foodTypesList.append(foodType)

    return foodTypesList