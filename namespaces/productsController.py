from bson import ObjectId  # Import ObjectId from the bson module
from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from apiModels.expect.productExpect import *
from apiModels.response.productResponse import *
from extensions import authorizations, db

nsProducts = Namespace(
    "products", authorizations=authorizations, description="Products operations"
)

productsCollection = db["products"]
tablesCollection = db["table"]



@nsProducts.route("/add")
class AddProductToTable(Resource):
    method_decorators = [jwt_required()]

    @nsProducts.doc(security="jsonWebToken")
    @nsProducts.expect(productPost)
    @nsProducts.marshal_with(productAdd)
    def post(self):
        product_data = api.payload
        tableId = product_data.get("table_id")
        print(tableId)
        # Ensure the table exists and retrieve it
        table = tablesCollection.find_one({"_id": ObjectId(tableId)})
        print(table)
        if table is None:
            abort(404, "Table not found")

        new_product = {
            "name": product_data["name"],
            "price": product_data["price"],
            "qty": product_data["qty"],
            "tableId": tableId,
        }

        # Calculate the product's total price and update the table's billValue
        product_price = new_product["price"] * new_product["qty"]
        table["billValue"] += product_price

        # Insert the new product into MongoDB
        product_id = productsCollection.insert_one(new_product).inserted_id

        # Update the table in MongoDB
        tablesCollection.update_one(
            {"_id": ObjectId(tableId)}, {"$set": {"billValue": table["billValue"]}}
        )

        new_product["_id"] = str(product_id)

        return new_product, 201


@nsProducts.route("/delall/<string:id>")
class DelProductToTable(Resource):

    def delete(self, id):    
        productDelete = productsCollection.find_one({"_id": ObjectId(id)})
        
        if productDelete is None:
            return abort(404, "There is no product with this id")

        table = tablesCollection.find_one({"_id": ObjectId(productDelete['tableId'])})
        print(table)
       
        table['billValue'] -= productDelete['price'] * productDelete['qty']
        #table['totalAmount'] -= productDelete['price'] * productDelete['qty']
        print(table)
        
        tablesCollection.update_one({"_id": ObjectId(productDelete['tableId'])}, {"$set": table})
        
       
        productsCollection.delete_one({"_id": ObjectId(id)})
        
        return {"Message": "Product deleted successfully"}, 201


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