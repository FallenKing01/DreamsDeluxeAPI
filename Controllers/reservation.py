from bson import ObjectId  # Import ObjectId from the bson module
from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from Domain.extensions import authorizations, db
from Infrastructure.Repositories.reservationRepo import *
from Models.expect.reservationExpect import *
from Models.response.reservationResponse import *
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
        try:

            reservation = postReservationRepo(nsReservation.payload,tableId)

            return reservation,201

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")



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
       try:
            restaurants = getReservationRepo()
            return restaurants, 200
       except Exception:
            abort(500, "Something went wrong")


@nsReservation.route("/searchRestaurant/<string:restaurantName>")
class SearchRestaurant(Resource):
    
    @nsReservation.doc(params={"restaurantName": "Restaurant name"})
    @nsReservation.marshal_with(reservationRestaurantResponse)
    def get(self, restaurantName):

        try:
            restaurants = searchRestaurantsRepo(restaurantName)
            return restaurants, 200
        except CustomException as ce:
            abort(ce.statusCode, ce.message)
        except Exception:
            abort(500, "Something went wrong")


