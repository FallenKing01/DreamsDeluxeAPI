from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from bson import ObjectId

from apiModels.expect.employerExpect import *
from apiModels.response.employerResponse import *
from extensions import authorizations, db


nsEmployer = Namespace("employer", authorizations=authorizations, description="Employer operations")

employerCollection = db["employers"]
userCollection = db["user"]



@nsEmployer.route("/create")
class CreateEmployer(Resource):
    method_decorators = [jwt_required()]

    @nsEmployer.doc(security="jsonWebToken")
    @nsEmployer.expect(employerExpect)
    @nsEmployer.marshal_with(employerResponse)
    def post(self):
        employerData = nsEmployer.payload
        user = userCollection.find_one({"_id": ObjectId(employerData["userId"])})
        print(user)
        if user is None:
            abort(404, "The user does not exist")
        
        if userCollection.find_one({"email": employerData["email"]}):
            abort(400, "The email is already used")
        
        newEmployer = {
            "name": employerData["name"],
            "email": employerData["email"],
            "password": employerData["password"],
            "role": employerData["role"],
            "salary": employerData["salary"],
            "birthdate": employerData["birthdate"],
            "userId": employerData["userId"],
            "income": 0,  
            "description": employerData["description"]
        }
        employerCollection.insert_one(newEmployer)
        
        newEmployeracc = {
            "email": employerData["email"],
            "password": employerData["password"],
            "role": employerData["role"],
            "income": 0  ,
            "imageUrl":"https://dreamsblob.blob.core.windows.net/profileimages/waiters-concept-illustration_114360-2908.avif",
        }
        userCollection.insert_one(newEmployeracc)
        
        return newEmployer, 200


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
    method_decorators = [jwt_required()]

    @nsEmployer.doc(security="jsonWebToken")
    @nsEmployer.doc(params={'id': 'User ID'})
    def delete(self, id):
        employer = employerCollection.find_one({"_id": ObjectId(id)})


        if not employer:
            abort(404, "Employer not found")

        employerCollection.delete_one({"_id": ObjectId(id)})
        userCollection.delete_one({"email":employer["email"]})

        return {"Message": "Employer deleted successfully"}, 200


@nsEmployer.route("/editemployer/<string:id>/<string:idEmployer>")
class EditEmployer(Resource):
    method_decorators = [jwt_required()]

    @nsEmployer.doc(security="jsonWebToken")
    @nsEmployer.doc(params={'id': 'User ID', 'idEmployer': 'Employer ID'})
    @nsEmployer.expect(editEmployer)
    def put(self, id, idEmployer):
        data = nsEmployer.payload
     
        employer = employerCollection.find_one({"_id":ObjectId(idEmployer),"userId":id})

        if not employer:
            abort(404, "Employer not found")

        employer["name"] = data.get('name')
        employer["password"] = data.get('password')
        employer["role"] = data.get('role')
        employer["salary"] = data.get('salary')
        employer["description"] = data.get('description')
        employer["birthdate"] = data.get('birthdate')
        

        employerCollection.update_one({"_id": ObjectId(idEmployer), "userId": id}, {"$set": employer})

        return {"message": "Employer data updated successfully"}, 200


@nsEmployer.route("/addincome/<string:id>/<float:income>")
class AddIncome(Resource):
    method_decorators = [jwt_required()]

    @nsEmployer.doc(security="jsonWebToken")
    @nsEmployer.doc(params={'id': 'Employer ID', 'income': 'Money'})
    def put(self, id, income):
        
        currentEmployer = employerCollection.find_one({"_id":ObjectId(id)})

        if not currentEmployer:
            abort(404, "Employer not found")

        employerCollection.update_one({"_id":ObjectId(id)},{"$inc":{"income" : income}})

        return {"Message": "Income added successfully"}, 200


@nsEmployer.route("/getEmployerByEmail/<string:email>")
class searchEmployer(Resource):
    #
    method_decorators = [jwt_required()]

    @nsEmployer.doc(security="jsonWebToken")
    @nsEmployer.doc(params={'email': 'Employer email'})
    @nsEmployer.marshal_list_with(employerResponse)

    def get(self, email):
        
        currentEmployer = employerCollection.find_one({"email":email})

        if not currentEmployer:
            abort(404, "Employer not found")

        return currentEmployer, 200