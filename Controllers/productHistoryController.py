from Infrastructure.Repositories.productsHistoryRepo import *
from flask_restx import Namespace, Resource
from Domain.extensions import authorizations
from Utils.Exceptions.customExceptions import CustomException
from flask import abort

nsProductHistory = Namespace("charts", authorizations=authorizations, description="Products operations")

@nsProductHistory.route("/sold/<string:adminId>/<string:startDate>/<string:endDate>")
class SoldProducts(Resource):
    def get(self, adminId , startDate , endDate):

        try:

            return getSoldProducts(adminId,startDate, endDate)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsProductHistory.route("/generalchart/<string:adminId>/<string:startDate>/<string:endDate>")
class GeneralChart(Resource):
    def get(self, adminId , startDate , endDate):

        try:

            return getGeneralChartRepo(adminId,startDate, endDate)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsProductHistory.route("/currentdaychart/<string:adminId>")
class CurrentDayChart(Resource):
    def get(self, adminId):

        try:

            return currentDayChartRepo(adminId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsProductHistory.route("/currentmonthchart1/<string:adminId>")
class CurrentMonthChart(Resource):
    def get(self, adminId):

        try:

            return currentMonthChartRepo(adminId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsProductHistory.route("/dailysalescurentmonth/<string:adminId>")
class DailySalesCurrentMonth(Resource):
    def get(self, adminId):

        try:

            return dailySalesForCurrentMonth(adminId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsProductHistory.route("/monthlysales/<string:adminId>")
class MonthlySales(Resource):
    def get(self, adminId):

        try:

            return salesForCurrentYear(adminId)

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")
