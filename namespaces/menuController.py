from bson import ObjectId  # Import ObjectId from the bson module
from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from apiModels.expect.productExpect import *
from apiModels.response.productResponse import *
from extensions import authorizations, db

usersCollection = db["user"]
menuCollection = db["menu"]


nsMenu = Namespace(
    "Menu", authorizations=authorizations, description="Menu operations"
)


@nsMenu.route("/addmenu/<string:adminId>")
class AddProductToMenu(Resource):
    method_decorators = [jwt_required()]
    @nsMenu.doc(security="jsonWebToken")
    @nsMenu.expect(productPostAdmin)
    @nsMenu.marshal_with(productAddAdmin)
    @nsMenu.doc(params={"adminId": "Admin ID"})
    def post(self,adminId):
        productData = api.payload
        admin = usersCollection.find_one({"_id": ObjectId(adminId)})
        if admin is None:
            abort(404, "Admin not found")
        newProduct = {
            "name": productData["name"].lower(),
            "price": productData["price"],
            "type": productData["type"],
            "adminId": adminId,
        }
        productId = menuCollection.insert_one(newProduct).inserted_id
        newProduct["_id"] = str(productId)
        
        return newProduct, 201

@nsMenu.route("/getproducts/<string:adminId>")
class GetProductsMenu(Resource):
    method_decorators = [jwt_required()]
    @nsMenu.doc(security="jsonWebToken")
    @nsMenu.marshal_with(productAddAdmin)
    @nsMenu.doc(params={"adminId": "Admin ID"})
    def get(self,adminId):
        admin = usersCollection.find_one({"_id": ObjectId(adminId)})
        if admin is None:
            abort(404, "Admin not found")
        products = menuCollection.find({"adminId": adminId})
        return list(products), 200

@nsMenu.route("deleteProd/<string:prodId>")
class DeleteProductMenu(Resource):
    method_decorators = [jwt_required()]
    @nsMenu.doc(security="jsonWebToken")
    @nsMenu.doc(params={"prodId": "Product ID"})
    def delete(self,prodId):
        product = menuCollection.find_one({"_id": ObjectId(prodId)})
        if product is None:
            abort(404, "Product not found")

        menuCollection.delete_one({"_id": ObjectId(prodId)})

        return "Message:Product deleted", 200



@nsMenu.route("/searchProduct/<string:productName>")
class SearchProductMenu(Resource):
    method_decorators = [jwt_required()]
    
    @nsMenu.doc(security="jsonWebToken")
    @nsMenu.doc(params={"productName": "Product name"})
    @nsMenu.marshal_with(productAddAdmin)
    def get(self, productName):
        # Perform a case-insensitive search on the lowercased product names
        products = menuCollection.find({
            "name": {"$regex": f".*{productName}.*", "$options": "i"},
        })

        # Convert MongoDB cursor to a list
        result = list(products)

        if not result:
            abort(404, f"No products found containing the word: {productName}")

        return result, 200
        
        