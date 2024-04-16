from bson import ObjectId
from Utils.Exceptions.customExceptions import CustomException
from Domain.extensions import tablesCollection, userCollection,productsCollection
from flask_jwt_extended import current_user, jwt_required

def createTableRepo(tableData,userId):

    # Ensure that the user exists in MongoDB

    user = userCollection.find_one({"_id": ObjectId(userId)})

    if user is None:
        raise CustomException(404, "The user does not exist")

    newTable = {
        "name": tableData["name"],
        "capacity": tableData.get("capacity"),
        "billValue": 0,
        "userId": str(userId),
    }

    insertedTable = tablesCollection.insert_one(newTable)
    insTableId = str(insertedTable.inserted_id)

    return insTableId

def getTablesOfUserRepo(id):

    tables = list(tablesCollection.find({"userId": id}))

    if not tables:
        raise CustomException(404, "Tables not found")

    for table in tables:
        table_id = table["_id"]

        products = list(productsCollection.find({"tableId": str(table_id)}))

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

    return tables

def getDetailsTableRepo(id):
    table = tablesCollection.find_one({"_id": ObjectId(id)})

    if not table:
        raise CustomException(404, "Table not found")

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

    return table

def deleteTableRepo(id):
    table = tablesCollection.find_one({"_id": ObjectId(id)})

    if table is None:
        raise CustomException(404, "Table not found")

    productsCollection.delete_many({"tableId": id})

    tablesCollection.delete_one({"_id": ObjectId(id)})

def resetTableDataRepo(id):
    table = tablesCollection.find_one({"_id": ObjectId(id)})

    if table is None:
        raise CustomException(404, "Table not found")

    bill_value = table['billValue']
    user_id = table['userId']

    userCollection.update_one(
        {"_id": ObjectId(user_id)},
        {"$inc": {"totalAmount": bill_value}}
    )

    # Reset table's bill value
    tablesCollection.update_one({"_id": ObjectId(id)}, {"$set": {"billValue": 0}})

    # Delete products associated with the table
    productsCollection.delete_many({"tableId": id})

