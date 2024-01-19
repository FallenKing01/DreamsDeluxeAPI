from bson import ObjectId  # Import ObjectId from the bson module
from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from extensions import authorizations, db
from apiModels.expect.reservationExpect import *
from apiModels.response.reservationResponse import *
import re

nsReservation = Namespace("reservation", description="Reservation operations")

reservationCollection = db["reservation"]
userCollection = db["user"]
tableCollection = db["table"]

@nsReservation.route("/postReservation/<string:tableId>/")
class postReservation(Resource):
    @nsReservation.expect( reservationExpect)
    @nsReservation.marshal_with(reservationResponse)
    @nsReservation.doc(params={"tableId": "Table id"})

    def post(self,tableId):
        reservationData = api.payload
        table = tableCollection.find_one({"_id": ObjectId(tableId)})
        if table is None:
            abort(404, "Table not found")

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

        return newReservation, 201


@nsReservation.route("/<string:tableId>/")
class getReservation(Resource):
    @nsReservation.marshal_with(reservationResponse)
    def get(self,tableId):
        table = tableCollection.find_one({"_id": ObjectId(tableId)})
        if table is None:
            abort(404, "Table not found")
        reservation = reservationCollection.find({"tableId": tableId})
        return list(reservation), 200


@nsReservation.route("/getRestaurants/")
class getRestaurants(Resource):
    @nsReservation.marshal_with(reservationRestaurantResponse)
    def get(self):
        restaurants = userCollection.find({"role": "admin"})

        return list(restaurants), 200


@nsReservation.route("/searchRestaurant/<string:restaurantName>")
class SearchRestaurant(Resource):
    
    @nsReservation.doc(params={"restaurantName": "Restaurant name"})
    @nsReservation.marshal_with(reservationRestaurantResponse)
    def get(self, restaurantName):
        
        restaurants = userCollection.find({
            "companyName": {"$regex": f".*{restaurantName}.*", "$options": "i"},
            "role": "admin"
        })

        result = list(restaurants)

        if not result:
            abort(404, f"No restaurants found containing the name: {restaurantName}")

        return result, 200


