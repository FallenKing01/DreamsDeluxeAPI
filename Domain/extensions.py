from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_restx import Api
from pymongo import MongoClient

api = Api()
jwt = JWTManager()

authorizations = {
    "jsonWebToken": {"type": "apiKey", "in": "header", "name": "Authorization"}
}


cluster = MongoClient(
    "mongodb+srv://Andrei:LsrbFqf9rk1fFZX5@dreamsdeluxe.x3fgxne.mongodb.net/"
)
db = cluster["dreamsDeluxe"]

userCollection = db["user"]
employersCollection = db["employers"]
menuCollection = db["menu"]
productsCollection = db["products"]
tablesCollection = db["table"]
reservationCollection = db["reservation"]
productsHistoryCollection = db["productHistory"]
tablesMapCollection = db["tableMap"]
