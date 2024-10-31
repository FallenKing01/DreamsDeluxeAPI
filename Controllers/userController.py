from bson import ObjectId
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from Models.expect.userExpect import *
from Models.response.userResponse import *
from Domain.extensions import authorizations,api
from urllib.parse import quote
from Infrastructure.Repositories.userRepo import *
from flask import abort
from Infrastructure.Repositories.employerRepo import deleteEmployeeRepo

nsUser = Namespace("user", authorizations=authorizations, description="User operations")

@nsUser.route("/getall")
class userAPI(Resource):

    method_decorators = [jwt_required()]
    @nsUser.doc(security="jsonWebToken")
    @nsUser.marshal_list_with(getUsers)
    def get(self):

        users = list(userCollection.find())

        return users



@nsUser.route("/create")
class userCreate(Resource):

    @nsUser.expect(userPost)
    def post(self):

        try:

            insertedId=createUserRepo(api.payload)

            return {"User id": insertedId}, 201

        except CustomException as ce:

            abort(ce.statusCode, ce.message)

        except Exception:

            abort(500, "Something went wrong")

@nsUser.route("/verifyuser/<string:email>")
class VerifyUser(Resource):

    @nsUser.doc(params={"email": "User email"})

    def get(self, email):

        try:

            verifyUserRepo(email)

            return  {"message": "You can create a user with this email"}, 200

        except CustomException as ce:

            abort(ce.statusCode, ce.message)

        except Exception:

            abort(500, "Something went wrong")


@nsUser.route("/getuser/<string:id>")

class GetUser(Resource):

    @nsUser.doc(params={"id": "User ID"})

    @nsUser.marshal_with(getUsers)

    def get(self, id):

        try:
            user = getUserByIdRepo(id)

            return user

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")
@nsUser.route("/getuserbyemail/<string:email>")
class getUserByEmail(Resource):

    @nsUser.doc(params={"email": "User email"})

    #@nsUser.marshal_with(getUsers)

    def get(self, email):

        try:

            user = getUserByEmailRepo(email)

            return user

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsUser.route("/deluser/<string:id>")
class DeleteUser(Resource):

    @nsUser.doc(params={"id": "User ID"})

    def delete(self, id):

        try:

            deleteEmployeeRepo(id)

            return {"message": "User deleted successfully"}, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsUser.route("/getuseradmin/<string:id>")
class GetUserAdmin(Resource):

    @nsUser.doc(params={"id": "User ID"})
    def get(self, id):

        try:

            adminId = getUserAdminRepo(id)

            return adminId

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")



@nsUser.route("/nume/<string:email>/<path:url>")
class ChangePhotoUrl(Resource):

    @nsUser.doc(params={"email": "User ID", "url": "Photo URL"})
    def put(self, email, url):
        
        # Find the user by ID
        user = userCollection.find_one({"email": email})

        if user is None:
            abort(404, "User not found")

        # URL decode the parameter
        decoded_url = quote(url, safe=':/')

        # Update the imageUrl using update_one
        userCollection.update_one({"email": email}, {"$set": {"imageUrl": decoded_url}})

        return {"message": "User updated successfully"}, 200

