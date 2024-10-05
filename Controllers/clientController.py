from flask_restx import Namespace, Resource
from Domain.extensions import authorizations,api
from flask import abort
from Utils.Exceptions.customExceptions import CustomException

from Models.expect.createClientExpect import *
from Models.expect.recensionExpect import *
from Infrastructure.Repositories.clientRepo import *
nsClient = Namespace("client", authorizations=authorizations, description="Client operations")


@nsClient.route("/create")
class userCreate(Resource):

    @nsClient.expect(clientPost)
    def post(self):
        try:
            insertedId=createClientRepo(api.payload)

            return {"User id": insertedId}, 201

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsClient.route("/getrestaurants/<string:county>/<string:location>")
class getRestaurants(Resource):
    def get(self,county,location):

        try:
            restaurants = getRestaurantsFromClientZoneRepo(county,location)

            return restaurants, 200

        except CustomException as ce:

            abort(ce.statusCode, ce.message)

        except Exception:

            abort(500, "Something went wrong")

@nsClient.route("/getproducts/<string:restaurantId>")
class getProducts(Resource):
    def get(self,restaurantId):

        try:
            products = getProductsFromRestaurant(restaurantId)

            return products, 200

        except CustomException as ce:

            abort(ce.statusCode, ce.message)

        except Exception:

            abort(500, "Something went wrong")

@nsClient.route("/postrecension")
class postRecension(Resource):

    @nsClient.expect(recensionPost)
    def post(self):
        try:
            message=postRecensionToRestaurant(api.payload)

            return message, 201

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsClient.route("/getrecensions/<string:restaurantId>")
class getRecensions(Resource):
    def get(self,restaurantId):

        try:
            recensions = getRecensionsOfRestaurant(restaurantId)

            return recensions, 200

        except CustomException as ce:

            abort(ce.statusCode, ce.message)

        except Exception:

            abort(500, "Something went wrong")