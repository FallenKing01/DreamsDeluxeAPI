from bson import ObjectId
from Utils.Exceptions.customExceptions import CustomException
from Domain.extensions import tablesCollection, userCollection,productsCollection,productsHistoryCollection
from datetime import datetime

def createTableRepo(tableData,userId):

    # Ensure that the user exists in MongoDB

    user = userCollection.find_one({"_id": ObjectId(userId)})

    if user is None:
        raise CustomException(404, "The user does not exist")

    if user["role"] == "admin":
        newTable = {
            "name": tableData["name"],
            "capacity": tableData.get("capacity"),
            "billValue": 0,
            "userId": str(userId),
        }

        insertedTable = tablesCollection.insert_one(newTable)
        insTableId = str(insertedTable.inserted_id)

    if user["role"] != "admin":
        newTable = {
            "name": tableData["name"],
            "capacity": tableData.get("capacity"),
            "billValue": 0,
            "userId": str(user["adminId"]),
        }

        insertedTable = tablesCollection.insert_one(newTable)
        insTableId = str(insertedTable.inserted_id)


    return insTableId


def getTablesOfUserRepo(id, page=1):
    limit = 9
    skip = (page - 1) * limit

    tables = list(tablesCollection.find({"userId": id}).sort([("name", 1)]).skip(skip).limit(limit))

    if not tables:
        raise CustomException(404, "Tables not found")

    for table in tables:
        table_id = table["_id"]

        products = list(productsCollection.find({"tableId": str(table_id)}))

        formated_products = []

        for product in products:

            currentProduct = {
                "id": str(product["_id"]),
                "name": product["name"],
                "price": product["price"],
                "qty": product["qty"]
            }
            formated_products.append(currentProduct)

        table["products"] = formated_products

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

    # Aggregate quantities and insert into productsHistoryCollection
    pipeline = [
        {"$match": {"tableId": id}},
        {"$group": {
            "_id": "$menuProductId",
            "totalQty": {"$sum": "$qty"},
            "userId": {"$first": "$userId"},  # Adding userId to the result
            "timeStamp": {"$first": datetime.utcnow()}
        }}
    ]

    aggregated_products = productsCollection.aggregate(pipeline)
    for product in aggregated_products:
        productsHistoryCollection.insert_one({
            "adminId": table["userId"],
            "menuProductId": product["_id"],
            "qty": product["totalQty"],
            "timeStamp": product["timeStamp"],
            "userId": product["userId"]
        })

    # Delete products associated with the table
    productsCollection.delete_many({"tableId": id})


def searchTableRepo(adminId, tableName):
    query = {"userId": adminId}
    response = []

    if tableName:
        # First, prioritize tables that start with the given tableName
        query["name"] = {"$regex": f"^{tableName}.*", "$options": "i"}
        tables = list(tablesCollection.find(query).limit(5))
    else:
        tables = list(tablesCollection.find(query).limit(5))

    if not tables:
        raise CustomException(404, "Table not found")

    # Remove 'products' key from each table in the result
    for table in tables:
        tableToAppend =  {
            "id": str(table["_id"]),
            "name": table["name"],
            "capacity": table["capacity"],
            "billValue": table["billValue"],
            "products": []
        }

        response.append(tableToAppend)

    return response






