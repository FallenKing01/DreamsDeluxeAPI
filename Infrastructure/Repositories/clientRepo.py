from Domain.extensions import userCollection,menuCollection,recensiosnsCollection
from Utils.Exceptions.customExceptions import CustomException
from bson import ObjectId
from Services.EmailSenderService import sendEmail
import bcrypt
from Domain.extensions import salt
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def checkUserExists(email):



    searchUser = userCollection.find_one({"email": email})

    if searchUser:

        return True

    return False


def createClientRepo(newClient):
    if checkUserExists(newClient["username"]):
        raise CustomException(409, "User with this email already exists")

    hashed_password = hash_password(newClient["password"])

    print(hashed_password +'!!!!!!!!!!!!!!!!')
    user = {
        "email": newClient["username"],
        "name": newClient["clientName"],
        "password": hashed_password,
        "role": "client",
        "phoneNumber": newClient["phoneNumber"],
        "location": newClient["location"],
        "county": newClient["county"],
    }

    insertedItm = userCollection.insert_one(user)
    insertedId = str(insertedItm.inserted_id)

    sendEmail(newClient["clientName"], "client", newClient["username"])

    return insertedId


def getRestaurantsFromClientZoneRepo(county, location):

    # Use $regex with 'i' option for case-insensitive comparison
    restaurants = list(userCollection.find({
        "location": {"$regex": f"^{location}$", "$options": "i"},
        "county": {"$regex": f"^{county}$", "$options": "i"},
        "role": "admin"
    }))

    for i in range(len(restaurants)):

        restaurants[i]["_id"] = str(restaurants[i]["_id"])
        restaurants[i].pop("password")
        restaurants[i].pop("role")
        restaurants[i].pop("totalRatings")

    return restaurants

def getProductsFromRestaurant(restaurantId):

    restaurant = userCollection.find_one({"_id": ObjectId(restaurantId)})

    if not restaurant:

        raise CustomException(404, "Restaurant not found")

    products = list(menuCollection.find({"adminId": restaurantId,"deleted":False}))

    for i in range(len(products)):

        products[i]["_id"] = str(products[i]["_id"])

    return products

def postRecensionToRestaurant(recension):

    recensiosnsCollection.insert_one(recension)

    restaurant = userCollection.find_one({"_id": ObjectId(recension["restaurantId"])})

    new_total_ratings = restaurant["totalRatings"] + [recension["rating"]]

    new_total_recensions = restaurant["totalRecensions"] + 1

    final_rating = sum(new_total_ratings) / new_total_recensions

    updateRestaurant = userCollection.update_one(
        {"_id": ObjectId(recension["restaurantId"])},
        {
            "$set": {
                "totalRatings": new_total_ratings,  # Update totalRatings with the new array
                "totalRecensions": new_total_recensions,  # Update totalRecensions
                "finalRating": final_rating  # Set the calculated finalRating
            }
        }
    )

    return {"message": "Recension posted successfully"}

def getRecensionsOfRestaurant(restaurantId):

    recensions = list(recensiosnsCollection.find({"restaurantId": restaurantId}))

    for i in range(len(recensions)):

        recensions[i]["_id"] = str(recensions[i]["_id"])

    return recensions


def updateClientLocationRepo(clientData):

    userExsit = userCollection.find_one({"_id": ObjectId(clientData["clientId"])})

    if userExsit is None:

        raise CustomException(404, "Client not found")

    userCollection.update_one(
        {"_id": ObjectId(clientData["clientId"])},
        {"$set": {"location": clientData["location"], "county": clientData["county"]}}
    )

    return {"message": "Location updated successfully"}

def getClientInfoRepo(clientId):

    user = userCollection.find_one({"_id": ObjectId(clientId)})

    if not user:

        raise CustomException(404, "Client not found")

    user["_id"] = str(user["_id"])
    user.pop("password")
    user.pop("role")

    return user