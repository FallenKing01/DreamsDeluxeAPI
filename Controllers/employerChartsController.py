from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from bson import ObjectId

from Domain.extensions import authorizations
from Infrastructure.Repositories.employerChartsRepo import *
nsChartEmployee = Namespace("employeecharts", authorizations=authorizations, description="Employer operations")

@nsChartEmployee.route("/dailymonthsales/<string:id>")
class DailyMonthSales(Resource):
    #method_decorators = [jwt_required()]

    #@nsChartEmployee.doc(security="jsonWebToken")
    @nsChartEmployee.doc(params={'id': 'User ID'})
    def get(self, id):

        try:

            sales = dailyEmployeeSalesForCurrentMonth(id)

        except Exception:

                abort(500, "Something went wrong")

        return sales, 200

@nsChartEmployee.route("/monthlychart/<string:id>")
class MonthlyChart(Resource):
    #method_decorators = [jwt_required()]

    #@nsChartEmployee.doc(security="jsonWebToken")
    @nsChartEmployee.doc(params={'id': 'User ID'})
    def get(self, id):

        try:

            sales = monthlyEmployeeSalesForCurrentYear(id)

        except Exception:

                abort(500, "Something went wrong")

        return sales, 200
