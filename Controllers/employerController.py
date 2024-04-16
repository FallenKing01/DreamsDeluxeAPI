from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from bson import ObjectId

from Models.expect.employerExpect import *
from Models.response.employerResponse import *
from Domain.extensions import authorizations, db
from Infrastructure.Repositories.userRepo import *
from Infrastructure.Repositories.employerRepo import *

nsEmployer = Namespace("employer", authorizations=authorizations, description="Employer operations")

employerCollection = db["employers"]
userCollection = db["user"]



@nsEmployer.route("/create")
class CreateEmployer(Resource):
    #method_decorators = [jwt_required()]
    #@nsEmployer.doc(security="jsonWebToken")
    @nsEmployer.expect(employerExpect)
    @nsEmployer.marshal_with(employerResponse)
    def post(self):
        try:
            employee = createEmployeeRepo(nsEmployer.payload)

            return employee,200


        except CustomException as ce:

            abort(ce.statusCode, ce.message)

        except Exception:

            abort(500, "Something went wrong")




@nsEmployer.route("/getemployers/<string:id>")
class GetEmployers(Resource):
    method_decorators = [jwt_required()]

    @nsEmployer.doc(security="jsonWebToken")
    @nsEmployer.doc(params={'id': 'User ID'})
    @nsEmployer.marshal_list_with(employerResponse)
    def get(self, id):
        employers = list(employerCollection.find({"userId":id}))

        if not employers:
            abort(404, "Employers not found")

        return employers, 200


@nsEmployer.route("/getemployer/<string:id>/<string:idEmployer>")
class GetEmployer(Resource):
    method_decorators = [jwt_required()]

    @nsEmployer.doc(security="jsonWebToken")
    @nsEmployer.doc(params={'id': 'User ID', 'idEmployer': 'Employer ID'})
    @nsEmployer.marshal_with(employerResponse)
    def get(self, id, idEmployer):
        employer = employerCollection.find_one({"_id": ObjectId(idEmployer), "userId": id})

        if not employer:
            abort(404, "Employer not found")

        return employer, 200



@nsEmployer.route("/delemployer/<string:id>")
class DeleteEmployer(Resource):
    #method_decorators = [jwt_required()]
    #@nsEmployer.doc(security="jsonWebToken")
    @nsEmployer.doc(params={'id': 'User ID'})
    def delete(self, id):

        try:
            deleteEmployeeRepo(id)

            return {"message": "Employer deleted successfully"}, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsEmployer.route("/editemployer/<string:id>/<string:idEmployer>")
class EditEmployer(Resource):
    #method_decorators = [jwt_required()]
    #@nsEmployer.doc(security="jsonWebToken")
    @nsEmployer.doc(params={'id': 'User ID', 'idEmployer': 'Employer ID'})
    @nsEmployer.expect(editEmployer)
    def put(self, id, idEmployer):

            try:

                editEmployeeRepo(nsEmployer.payload, id, idEmployer)

                return {"message": "Employer data updated successfully"}, 200
            except CustomException as ce:
                abort(ce.statusCode, ce.message)

            except Exception:
                abort(500, "Something went wrong")


@nsEmployer.route("/addincome/<string:id>/<float:income>")
class AddIncome(Resource):
    #method_decorators = [jwt_required()]

    #@nsEmployer.doc(security="jsonWebToken")
    @nsEmployer.doc(params={'id': 'Employer ID', 'income': 'Money'})
    def put(self, id, income):
        
        try:
            addIncomeRepo(id, income)

            return {"message": "Income added successfully"}, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")


@nsEmployer.route("/getEmployerByEmail/<string:email>")
class searchEmployer(Resource):
    #method_decorators = [jwt_required()]

    #@nsEmployer.doc(security="jsonWebToken")
    @nsEmployer.doc(params={'email': 'Employer email'})
    @nsEmployer.marshal_list_with(employerResponse)

    def get(self, email):
        
        try:
            employee = getEmployeesByEmailRepo(email)

            return employee, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")