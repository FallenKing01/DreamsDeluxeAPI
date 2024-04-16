from bson import ObjectId  # Import ObjectId from the bson module
from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from Infrastructure.Repositories.menuRepo import *
from Models.expect.productExpect import *
from Models.response.productResponse import *
from Domain.extensions import authorizations, db




nsMenu = Namespace(
    "menu", authorizations=authorizations, description="Menu operations"
)


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

@nsMenu.route("/getproducts/<string:adminId>")
class GetProductsMenu(Resource):
    #method_decorators = [jwt_required()]
    #@nsMenu.doc(security="jsonWebToken")
    @nsMenu.marshal_with(productAddAdmin)
    @nsMenu.doc(params={"adminId": "Admin ID"})
    def get(self,adminId):

        try:
              products = getProductsFromMenuRepo(adminId)
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




@nsMenu.route("/searchProduct/<string:productName>")
class SearchProductMenu(Resource):
    #method_decorators = [jwt_required()]
    
    #@nsMenu.doc(security="jsonWebToken")
    @nsMenu.doc(params={"productName": "Product name"})
    @nsMenu.marshal_with(productAddAdmin)
    def get(self, productName):

        try:

            products = searchProductFromMenuRepo(productName)
            return products, 200

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")
        
        