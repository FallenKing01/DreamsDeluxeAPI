from bson import ObjectId  # Import ObjectId from the bson module
from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from Infrastructure.Repositories.productRepo import *
from Utils.Exceptions.customExceptions import CustomException
from Models.expect.productExpect import *
from Models.response.productResponse import *
from Domain.extensions import authorizations, db

nsProducts = Namespace(
    "products", authorizations=authorizations, description="Products operations"
)

productsCollection = db["products"]
tablesCollection = db["table"]
employersCollection = db["employers"]
usersCollection = db["user"]


@nsProducts.route("/add/<string:id>")

class AddProductToTable(Resource):
    #method_decorators = [jwt_required()]

    #@nsProducts.doc(security="jsonWebToken")
    @nsProducts.expect(productPost)
    @nsProducts.marshal_with(productAdd)
    @nsProducts.doc(params={"id": "Employer ID"})
    def post(self,id):

        try:

            productData = addProductToTableRepo(nsProducts.payload,id)

            return productData,201

        except CustomException as ce:
            abort(ce.status_code, ce.message)
        except Exception as e:
            abort(500, str(e))



@nsProducts.route("/delall/<string:id>")
class DelProductToTable(Resource):
    @nsProducts.doc(params={"id": "Product ID"})
    def delete(self, id):

        try:
            delProductToTableRepo(id)
            return {"Message": "Product deleted successfully"}, 201

        except CustomException as ce:
            abort(ce.status_code, ce.message)

        except Exception as e:
            abort(500, str(e))

@nsProducts.route("/delqty/<string:id>/<int:qty>")
class DelProductQuantity(Resource):
    method_decorators = [jwt_required()]
    @nsProducts.doc(security="jsonWebToken")
    def delete(self,id, qty):
       
        productDelete = productsCollection.find_one({"_id": ObjectId(id)})

        if productDelete is None:
            return abort(404, "There is no product with this id")

        if qty <= 0:
            return abort(400, "Quantity must be greater than zero")

        if qty > productDelete['qty']:
            return abort(400, "Quantity to delete exceeds available quantity")

        deleted_price = productDelete['price'] * qty

        table = tablesCollection.find_one({"_id": ObjectId(productDelete['tableId'])})

        if table is None:
            return abort(404, "Table not found for this product")

        table['billValue'] -= deleted_price
        productDelete['qty'] -= qty

        if productDelete['qty'] == 0:
            productsCollection.delete_one({"_id": ObjectId(id)})
        else:
            productsCollection.update_one({"_id": ObjectId(id)}, {"$set": productDelete})

        tablesCollection.update_one({"_id": ObjectId(productDelete['tableId'])}, {"$set": table})

        return {"Message": f"{qty} products deleted successfully"}, 201


