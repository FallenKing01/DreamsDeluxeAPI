from bson import ObjectId
from Utils.Exceptions.customExceptions import CustomException
from Domain.extensions import tablesCollection,reservationCollection,userCollection
def postReservationRepo(reservationData,tableId):


    table = tablesCollection.find_one({"_id": ObjectId(tableId)})
    if table is None:
        raise CustomException(404, "Table not found")

    newReservation = {
        "tableId": tableId,
        "reservationName": reservationData["reservationName"],
        "startTime": reservationData["startTime"],
        "endTime": reservationData["endTime"],
        "guests": reservationData["guests"],
        "specialRequests": reservationData["specialRequests"],
    }
    reservationId = reservationCollection.insert_one(newReservation).inserted_id
    newReservation["_id"] = str(reservationId)

    return newReservation

def getReservationRepo():

    restaurants = userCollection.find({"role": "admin"})

    return list(restaurants)

def searchRestaurantsRepo(restaurantName):

    restaurants = userCollection.find({
        "companyName": {"$regex": f".*{restaurantName}.*", "$options": "i"},
        "role": "admin"
    })

    result = list(restaurants)

    if not result:
        raise CustomException(404, f"No restaurants found containing the name: {restaurantName}")

    return result