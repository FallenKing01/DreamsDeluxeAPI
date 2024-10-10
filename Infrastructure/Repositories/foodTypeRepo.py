from Domain.extensions import foodTypeCollection,userCollection
from Utils.Exceptions.customExceptions import CustomException
from bson import ObjectId

def createFoodTypeRepo(foodType):

    insertedType = foodTypeCollection.insert_one(foodType)

    response = {
        "name" : foodType["typeName"],
        "id" : str(insertedType.inserted_id)
    }

    return response

def getFoodTypesRepo():



    foodTypes = foodTypeCollection.find()

    foodTypesList = []

    for foodType in foodTypes:

        foodType['_id'] = str(foodType['_id'])

        if 'adminId' in foodType:

            foodType['adminId'] = str(foodType['adminId'])

        foodTypesList.append(foodType)

    return foodTypesList