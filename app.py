from bson import ObjectId
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
import os

from extensions import api, db, jwt  

from namespaces.userController import nsUser



app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://Andrei:LsrbFqf9rk1fFZX5@dreamsdeluxe.x3fgxne.mongodb.net/?retryWrites=true&w=majority"
app.config["JWT_SECRET_KEY"] = "cookiemonster"

collection = db["user"]


api.init_app(app)



api.add_namespace(nsUser)




print(app.config["MONGO_URI"])

mongo = PyMongo(app)
jwt = JWTManager(app)


# JWT Identity Loader
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user["id"]


# JWT User Lookup Callback
@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data):
    identity = jwt_data["sub"]

    user = collection.find_one({"_id": ObjectId(identity)})
    return user


if __name__ == "__main__":
    app.run()
