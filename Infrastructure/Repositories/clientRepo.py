from Domain.extensions import userCollection,menuCollection,recensiosnsCollection
from Utils.Exceptions.customExceptions import CustomException
from bson import ObjectId

def checkUserExists(email):



    searchUser = userCollection.find_one({"email": email})

    if searchUser:

        return True

    return False


def createClientRepo(newClient):

    if checkUserExists(newClient["username"]):

        raise CustomException(409, "User with this email already exists")

    user = {
        "email": newClient["username"],
        "password": newClient["password"],
        "role": "client",
        "phoneNumber": newClient["phoneNumber"],
        "location": newClient["location"],
        "county": newClient["county"],
    }

    insertedItm = userCollection.insert_one(user)
    insertedId = str(insertedItm.inserted_id)

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

    products = list(menuCollection.find({"adminId": restaurantId}))

    for i in range(len(products)):

        products[i]["_id"] = str(products[i]["_id"])

    return products

def postRecensionToRestaurant(recension):

    # Insert the new recension into the recensiosnsCollection
    recensiosnsCollection.insert_one(recension)

    # Fetch the current restaurant document to calculate the new final rating
    restaurant = userCollection.find_one({"_id": ObjectId(recension["restaurantId"])})

    # Append the new rating to the totalRatings array
    new_total_ratings = restaurant["totalRatings"] + [recension["rating"]]

    # Increment totalRecensions
    new_total_recensions = restaurant["totalRecensions"] + 1

    # Calculate the new average rating (finalRating)
    final_rating = sum(new_total_ratings) / new_total_recensions

    # Update the restaurant document with the new values
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
