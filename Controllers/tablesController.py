from bson import ObjectId
from flask import abort
from flask_jwt_extended import current_user, jwt_required
from flask_restx import Namespace, Resource

from Infrastructure.Repositories.tablesRepo import *
from Models.expect.tableExpect import tablePost
from Models.response.tableResponse import *
from Domain.extensions import authorizations, db

tableCollection = db["table"]
userCollection = db["user"]
productsCollection = db["products"]

nsTables = Namespace(
    "tables", authorizations=authorizations, description="Tables opperations"
)


@nsTables.route("/create/<string:userId>")
class TableAPI(Resource):
    method_decorators = [jwt_required()]


    @nsTables.doc(security="jsonWebToken")
    @nsTables.expect(tablePost)
    def post(self, userId):
        try:

            insTableId = createTableRepo(nsTables.payload,userId)

            return {"Table id": insTableId}, 201

        except CustomException as ce:
            abort(ce.statusCode, ce.message)

        except Exception:
            abort(500, "Something went wrong")

@nsTables.route("/gettables/<string:id>/<int:page>")
class GetTables(Resource):
   # method_decorators = [jwt_required()]

    @nsTables.doc(security="jsonWebToken")
    @nsTables.doc(params={"id": "User ID"})
    @nsTables.marshal_list_with(tableget)
    def get(self, id, page):
        try:
            tables = getTablesOfUserRepo(id,page)

            return tables, 200
        except CustomException as ce:(
            abort(ce.statusCode, ce.message))

        except Exception:
            abort(500, "Something went wrong")


@nsTables.route("/gettable/<string:id>")
class GetTable(Resource):
    method_decorators = [jwt_required()]

    @nsTables.doc(security="jsonWebToken")
    @nsTables.doc(params={"id": "Table ID"})
    @nsTables.marshal_with(tableget)
    def get(self, id):
        try:
            table = getDetailsTableRepo(id)
            return table, 200
        except CustomException as ce:
            abort(ce.statusCode, ce.message)
        except Exception:
            abort(500, "Something went wrong")


@nsTables.route("/delete/<string:id>")
class DeleteTable(Resource):
    method_decorators = [jwt_required()]

    @nsTables.doc(security="jsonWebToken")
    def delete(self, id):

        try:
            deleteTableRepo(id)
            return {"message": "Table and associated products deleted successfully"}, 200
        except CustomException as ce:
            abort(ce.statusCode, ce.message)
        except Exception:
            abort(500, "Something went wrong")


@nsTables.route("/reset/<string:id>")
class ResetTable(Resource):

    @jwt_required()
    @nsTables.doc(security="jsonWebToken")
    def put(self, id):
       
            try:

                resetTableDataRepo(id)
                return {"Message": "The table was reset successfully"}, 200

            except CustomException as ce:
                abort(ce.statusCode, ce.message)
            except Exception:
                abort(500, "Something went wrong")

@nsTables.route("/search/<string:adminId>/<string:tableName>")
class SearchTable(Resource):
    #method_decorators = [jwt_required()]

    #@nsTables.doc(security="jsonWebToken")
    @nsTables.doc(params={"adminId": "Admin ID", "tableName": "Table Name"})
    def get(self, adminId, tableName):
        try:
            tables = searchTableRepo(adminId, tableName)
            return tables, 200
        except CustomException as ce:
            abort(ce.statusCode, ce.message)
        except Exception:
            abort(500, "Something went wrong")