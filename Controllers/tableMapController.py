from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from bson import ObjectId

from Models.expect.tablesMapExpect import tableMapExpect
from Domain.extensions import authorizations
from Infrastructure.Repositories.tablesMapRepo import *

nsTableMap = Namespace("tablemap", authorizations=authorizations, description="Table map operations")

@nsTableMap.route("/update/<string:adminId>")
class UpdateTableMap(Resource):
    #method_decorators = [jwt_required()]
    #@nsTableMap.doc(security="jsonWebToken")
    @nsTableMap.expect(tableMapExpect)
    def put(self, adminId):
        try:

            response = updateTableMapRepo(adminId,nsTableMap.payload)

            return response, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

