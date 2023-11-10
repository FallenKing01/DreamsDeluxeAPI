from bson import ObjectId
from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from apiModels.expect.userExpect import *
from apiModels.response.userResponse import *
from extensions import authorizations, db


nsUser = Namespace("user", authorizations=authorizations, description="User operations")

userCollection = db["user"]



@nsUser.route("/getall")

class userAPI(Resource):

    method_decorators = [jwt_required()]


    @nsUser.doc(security="jsonWebToken")

    @nsUser.marshal_list_with(getUsers)

    def get(self):

        users = list(userCollection.find())
        return users



@nsUser.route("/create")

class userAPI(Resource):

    @nsUser.expect(userPost)
    def post(self):

        user = userCollection.find_one({"email": nsUser.payload["username"]})
        if user:

            abort(409, "User with this email already exists")


        # Create a new user

        user = {

            "email": nsUser.payload["username"],

            "password": nsUser.payload["password"],

            "role": nsUser.payload["role"],

            "totalAmount": 0,

        }


        insertedItm = userCollection.insert_one(user)

        insertedId = str(insertedItm.inserted_id)


        return {"User id": insertedId}, 201



@nsUser.route("/getuser/<string:id>")

class GetUser(Resource):

    @nsUser.doc(params={"id": "User ID"})

    @nsUser.marshal_with(getUsers)

    def get(self, id):

        if len(id) == 24 and all(c in "0123456789abcdefABCDEF" for c in id):

            user = userCollection.find_one({"_id": ObjectId(id)})


            if user is None:

                abort(404, "User not found")

            return user
        else:

            abort(400, "Invalid user ID")



@nsUser.route("/deluser/<string:id>")

class DeleteUser(Resource):

    @nsUser.doc(params={"id": "User ID"})

    def delete(self, id):

        obj_id = ObjectId(id)

        user = userCollection.find_one({"_id": obj_id})


        if user is None:

            abort(404, "User not found")

        userCollection.delete_one({"_id": obj_id})


        return {"message": "User deleted successfully"}, 200

