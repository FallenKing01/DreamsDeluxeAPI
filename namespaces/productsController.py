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
employersCollection = db["employers"]
usersCollection = db["user"]
menuCollection = db["menu"]

@nsProducts.route("/add/<string:id>")

class AddProductToTable(Resource):
    method_decorators = [jwt_required()]

    @nsProducts.doc(security="jsonWebToken")
    @nsProducts.expect(productPost)
    @nsProducts.marshal_with(productAdd)
    @nsProducts.doc(params={"id": "Employer ID"})
    def post(self,id):
        product_data = api.payload
        tableId = product_data.get("table_id")
       
        table = tablesCollection.find_one({"_id": ObjectId(tableId)})
        
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

        findUser = usersCollection.find_one({"_id": ObjectId(id)})
        print(findUser)
        employersCollection.update_one({"email": findUser["email"]}, {"$inc": {"income": product_price}})
       
       
        return new_product, 201


@nsProducts.route("/delall/<string:id>/<string:employerId>")
class DelProductToTable(Resource):
    @nsProducts.doc(params={"id": "Product ID"})
    @nsProducts.doc(params={"employerId": "Employer ID"})
    def delete(self, id, employerId):    
        productDelete = productsCollection.find_one({"_id": ObjectId(id)})
        
        if productDelete is None:
            return abort(404, "There is no product with this id")

        product_price=productDelete['price'] * productDelete['qty']*(-1)
        table = tablesCollection.find_one({"_id": ObjectId(productDelete['tableId'])})
        
       
        table['billValue'] -= productDelete['price'] * productDelete['qty']    
        
        tablesCollection.update_one({"_id": ObjectId(productDelete['tableId'])}, {"$set": table})
        
        findUser = usersCollection.find_one({"_id": ObjectId(employerId)})
        
        employersCollection.update_one({"email": findUser["email"]}, {"$inc": {"income": product_price}})
       
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

#############################################################################################################
#Admin adding products in the menu 
#############################################################################################################
@nsProducts.route("/addmenu/<string:adminId>")
class AddProductToMenu(Resource):
    method_decorators = [jwt_required()]
    @nsProducts.doc(security="jsonWebToken")
    @nsProducts.expect(productPostAdmin)
    @nsProducts.marshal_with(productAddAdmin)
    @nsProducts.doc(params={"adminId": "Admin ID"})
    def post(self,adminId):
        productData = api.payload
        admin = usersCollection.find_one({"_id": ObjectId(adminId)})
        if admin is None:
            abort(404, "Admin not found")
        newProduct = {
            "name": productData["name"],
            "price": productData["price"],
            "type": productData["type"],
            "adminId": adminId,
        }
        productId = menuCollection.insert_one(newProduct).inserted_id
        newProduct["_id"] = str(productId)
        
        return newProduct, 201