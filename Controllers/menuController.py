from bson import ObjectId  # Import ObjectId from the bson module
from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from Infrastructure.Repositories.menuRepo import *
from Models.expect.productExpect import *
from Models.response.productResponse import *
from Domain.extensions import authorizations, db




nsMenu = Namespace("menu", authorizations=authorizations, description="Menu operations")


@nsMenu.route("/addmenu/<string:adminId>")
class AddProductToMenu(Resource):
    #method_decorators = [jwt_required()]
    #@nsMenu.doc(security="jsonWebToken")
    @nsMenu.expect(productPostAdmin)
    @nsMenu.marshal_with(productAddAdmin)
    @nsMenu.doc(params={"adminId": "Admin ID"})
    def post(self,adminId):

        try:

            newProduct = addProductInMenuRepo(nsMenu.payload, adminId)

            return newProduct, 201

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsMenu.route("/getproducts/<string:adminId>/<int:page>")
class GetProductsMenu(Resource):
    #method_decorators = [jwt_required()]
    #@nsMenu.doc(security="jsonWebToken")
    @nsMenu.marshal_with(productAddAdmin)
    @nsMenu.doc(params={"adminId": "Admin ID"})
    def get(self,adminId, page):

        try:

              products = getProductsFromMenuRepo(adminId, page)
              return products, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsMenu.route("deleteProd/<string:prodId>")
class DeleteProductMenu(Resource):
    #method_decorators = [jwt_required()]
    #@nsMenu.doc(security="jsonWebToken")
    @nsMenu.doc(params={"prodId": "Product ID"})
    def delete(self,prodId):

        try:

            deleteProductFromMenuRepo(prodId)
            return {"Message": "Product deleted successfully"}, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsMenu.route("/updateproduct/<string:prodId>")
class UpdateProductMenu(Resource):
    @nsMenu.expect(productPostAdmin)
    #method_decorators = [jwt_required()]
    #@nsMenu.doc(security="jsonWebToken")
    def put(self,prodId):

        try:

            updateProductMenuRepo(nsMenu.payload, prodId)
            return {"Message": "Product updated successfully"}, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsMenu.route("/searchproduct/<string:adminId>/<string:productName>")
class SearchProductMenu(Resource):
    #method_decorators = [jwt_required()]
    #@nsMenu.doc(security="jsonWebToken")
    @nsMenu.doc(params={"adminId": "Admin ID", "productName": "Product name"})
    @nsMenu.marshal_with(productAddAdmin)
    def get(self, adminId, productName):

        try:

            products = searchProductInMenuRepo(adminId, productName)
            return products, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")