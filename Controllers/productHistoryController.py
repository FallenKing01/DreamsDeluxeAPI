from Infrastructure.Repositories.productsHistoryRepo import getSoldProducts
from flask_restx import Namespace, Resource
from Domain.extensions import authorizations
from Utils.Exceptions.customExceptions import CustomException
from flask import abort

nsProductHistory = Namespace("producthistory", authorizations=authorizations, description="Products operations")

@nsProductHistory.route("/sold/<string:adminId>/<string:startDate>/<string:endDate>")
class SoldProducts(Resource):
    def get(self, adminId , startDate , endDate):

        try:

            return getSoldProducts(adminId,startDate, endDate)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

