from bson import ObjectId
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
import os
from flask_cors import CORS 
from Domain.extensions import api, db, jwt

from Controllers.userController import nsUser
from Controllers.tablesController import nsTables
from Controllers.productsController import nsProducts
from Controllers.loginController import nsLogin
from Controllers.employerController import nsEmployer
from Controllers.uploadController import nsUpload
from Controllers.menuController import nsMenu
from Controllers.reservation import nsReservation
from Controllers.tableMapController import nsTableMap
from Controllers.productHistoryController import nsProductHistory
from Controllers.employerChartsController import nsChartEmployee
from Controllers.foodTypeController import nsFoodType
from Controllers.clientController import nsClient
from Controllers.regionCotroller import nsRegion

app = Flask(__name__)
CORS(app)


app.config["MONGO_URI"] = "mongodb+srv://Andrei:LsrbFqf9rk1fFZX5@dreamsdeluxe.x3fgxne.mongodb.net/?retryWrites=true&w=majority"
app.config["JWT_SECRET_KEY"] = "cookiemonster"



collection = db["user"]

api.init_app(app)
api.add_namespace(nsUser)
api.add_namespace(nsLogin)
api.add_namespace(nsTables)
api.add_namespace(nsProducts)
api.add_namespace(nsEmployer)
api.add_namespace(nsUpload)
api.add_namespace(nsMenu)
api.add_namespace(nsReservation)
api.add_namespace(nsTableMap)
api.add_namespace(nsProductHistory)
api.add_namespace(nsChartEmployee)
api.add_namespace(nsFoodType)
api.add_namespace(nsClient)
api.add_namespace(nsRegion)

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
    app.run(debug=True)