from bson import ObjectId
from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from apiModels.expect.userExpect import *
from apiModels.response.userResponse import *
from extensions import authorizations, db
from urllib.parse import quote


nsUser = Namespace("user", authorizations=authorizations, description="User operations")

userCollection = db["user"]
employersCollection = db["employers"]



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
            
            "imageUrl": "https://dreamsblob.blob.core.windows.net/profileimages/d9e0d9f0-d02c-4bce-9f14-82464104f74b"

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

@nsUser.route("/getuserbyemail/<string:email>")
class getUserByEmail(Resource):

    @nsUser.doc(params={"email": "User email"})

    @nsUser.marshal_with(getUsers)

    def get(self, email):


            user = userCollection.find_one({"email": email})


            if user is None:

                abort(404, "User not found")

            return user


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

@nsUser.route("/getuseradmin/<string:id>")
class GetUserAdmin(Resource):

    @nsUser.doc(params={"id": "User ID"})

   

    def get(self, id):

        if len(id) == 24 and all(c in "0123456789abcdefABCDEF" for c in id):

            user = userCollection.find_one({"_id": ObjectId(id)})
       

            if user is None:

                abort(404, "User not found")
            
            admin = employersCollection.find_one({'email': user["email"]})
           
            if admin is None:             
                abort(404, "Admin not found")

            return {"id": admin["userId"]}

            
        else:

            abort(400, "Invalid user ID")



@nsUser.route("/nume/<string:email>/<path:url>")
class ChangePhotoUrl(Resource):

    @nsUser.doc(params={"email": "User ID", "url": "Photo URL"})
    def put(self, email, url):
        # Convert the string id to ObjectId
       
        
        # Find the user by ID
        user = userCollection.find_one({"email": email})

        if user is None:
            abort(404, "User not found")

        # URL decode the parameter
        decoded_url = quote(url, safe=':/')

        # Update the imageUrl using update_one
        userCollection.update_one({"email": email}, {"$set": {"imageUrl": decoded_url}})

        return {"message": "User updated successfully"}, 200

