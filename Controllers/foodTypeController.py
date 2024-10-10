from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from bson import ObjectId
from Utils.Exceptions.customExceptions import CustomException
from Domain.extensions import authorizations
from Models.expect.foodTypeExpect import *
from Infrastructure.Repositories.foodTypeRepo import *

nsFoodType = Namespace("foodtype", authorizations=authorizations, description="Food type operations")

@nsFoodType.route("/create")
@nsFoodType.expect(foodTypePost)
# method_decorators = [jwt_required()]
# @nsEmployer.doc(security="jsonWebToken")
class CreateFoodType(Resource):
    def post(self):

        try:

            foodType = createFoodTypeRepo(nsFoodType.payload)

            return foodType, 200

        except CustomException as ce:

            abort(ce.statusCode, ce.message)

        except Exception:

            abort(500, "Something went wrong")

@nsFoodType.route("/getfoodtypes")

class GetFoodTypes(Resource):

    def get(self):

        try:

            foodTypes = getFoodTypesRepo()

            return foodTypes,200

        except CustomException as ce:

            abort(ce.statusCode, ce.message)

        except Exception:

            abort(500, "Something went wrong")



