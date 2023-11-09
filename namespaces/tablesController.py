from bson import ObjectId
from flask import abort
from flask_jwt_extended import current_user, jwt_required
from flask_restx import Namespace, Resource

from apiModels.expect.tableExpect import tablePost
from apiModels.response.tableResponse import *
from extensions import authorizations, db

tableCollection = db["table"]
userCollection = db["user"]
productsCollection = db["products"]

nsTables = Namespace(
    "tables", authorizations=authorizations, description="Tables opperations"
)


@nsTables.route("/create")
class TableAPI(Resource):
    method_decorators = [jwt_required()]

    @nsTables.doc(security="jsonWebToken")
    @nsTables.expect(tablePost)
    def post(self):
        tableData = nsTables.payload

        # Ensure that the user exists in MongoDB
        userId = current_user["_id"]
        user = userCollection.find_one({"_id": ObjectId(userId)})

        if user is None:
            abort(404, "The user does not exist")

        newTable = {
            "name": tableData["name"],
            "capacity": tableData.get("capacity"),
            "billValue": 0,
            "userId": str(userId),
        }

        insertedTable = tableCollection.insert_one(newTable)
        insTableId = str(insertedTable.inserted_id)
        return {"Table id": insTableId}, 201


@nsTables.route("/gettables/<string:id>")
class GetTables(Resource):
    method_decorators = [jwt_required()]

    @nsTables.doc(security="jsonWebToken")
    @nsTables.doc(params={"id": "User ID"})
    @nsTables.marshal_list_with(tableget)
    def get(self, id):
        # Fetch tables associated with the user
        tables = list(tableCollection.find({"userId": id}))

        if not tables:
            abort(404, "Tables not found")

        # Fetch and format associated product data for each table
        for table in tables:
            table_id = table["_id"]

            # Fetch associated products for the table
            products = list(productsCollection.find({"tableId": str(table_id)}))

            # Create a list to store the formatted product data
            formatted_products = []

            # Format each product and append it to the list
            for product in products:
                formatted_product = {
                    "id": str(product["_id"]),
                    "name": product["name"],
                    "price": product["price"],
                    "qty": product["qty"],
                }
                formatted_products.append(formatted_product)

            # Update the "products" field in the table data
            table["products"] = formatted_products

        return tables, 200


@nsTables.route("/gettable/<string:id>")
class GetTable(Resource):
    method_decorators = [jwt_required()]

    @nsTables.doc(security="jsonWebToken")
    @nsTables.doc(params={"id": "Table ID"})
    @nsTables.marshal_with(tableget)
    def get(self, id):
        table = tableCollection.find_one({"_id": ObjectId(id)})

        if not table:
            abort(404, "Table not found")

        products = list(productsCollection.find({"tableId": str(id)}))

        formatted_products = []

        for product in products:
            formatted_product = {
                "id": str(product["_id"]),
                "name": product["name"],
                "price": product["price"],
                "qty": product["qty"],
            }
            formatted_products.append(formatted_product)

        table["products"] = formatted_products

        return table, 200


@nsTables.route("/delete/<string:id>")
class DeleteTable(Resource):
    method_decorators = [jwt_required()]

    @nsTables.doc(security="jsonWebToken")
    def delete(self, id):
        table = tableCollection.find_one({"_id": ObjectId(id)})

        if table is None:
            abort(404, "Table not found")

        productsCollection.delete_many({"tableId": id})

        tableCollection.delete_one({"_id": ObjectId(id)})

        return {"message": "Table and associated products deleted successfully"}, 200


@nsTables.route("/reset/<string:id>")
class ResetTable(Resource):

    @jwt_required()
    @nsTables.doc(security="jsonWebToken")
    def put(self, id):
       
            table = tableCollection.find_one({"_id": ObjectId(id)})

            if table is None:
                abort(404, "Table not found")

            bill_value = table['billValue']
            user_id = table['userId']

            # Print for debugging
            print("User ID:", user_id)
            print("Bill Value:", bill_value)

            userCollection.update_one(
                {"_id": ObjectId(user_id)},
                {"$inc": {"totalAmount": bill_value}}
            )
            
            # Reset table's bill value
            tableCollection.update_one({"_id": ObjectId(id)}, {"$set": {"billValue": 0}})

            # Delete products associated with the table
            productsCollection.delete_many({"tableId": id})

            return {"Message": "The table was reset successfully"}, 200
