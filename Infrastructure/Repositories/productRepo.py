
from Domain.extensions import  tablesCollection,productsCollection,employersCollection,userCollection
from bson import ObjectId
from Utils.Exceptions.customExceptions import CustomException

def addProductToTableRepo(productData,id):

    tableId = productData.get("table_id")

    table = tablesCollection.find_one({"_id": ObjectId(tableId)})
    print(table)
    if table is None:
        raise CustomException(404, "Table not found")

    newProduct = {

        "name": productData["name"],
        "price": productData["price"],
        "qty": productData["qty"],
        "tableId": tableId,
        "menuProductId": productData["menuProductId"],
        "userId": id
    }

    # Calculate the product's total price and update the table's billValue
    product_price = newProduct["price"] * newProduct["qty"]
    table["billValue"] += product_price

    # Insert the new product into MongoDB
    productId = productsCollection.insert_one(newProduct).inserted_id

    # Update the table in MongoDB
    tablesCollection.update_one(
        {"_id": ObjectId(tableId)}, {"$set": {"billValue": table["billValue"]}}
    )

    newProduct["_id"] = str(productId)

    findUser = userCollection.find_one({"_id": ObjectId(id)})

    employersCollection.update_one({"email": findUser["email"]}, {"$inc": {"income": product_price}})

    return newProduct

def delProductToTableRepo(id):

    productDelete = productsCollection.find_one({"_id": ObjectId(id)})

    if productDelete is None:
        raise CustomException(404, "There is no product with this id")

    product_price = productDelete['price'] * productDelete['qty'] * (-1)
    table = tablesCollection.find_one({"_id": ObjectId(productDelete['tableId'])})

    table['billValue'] -= productDelete['price'] * productDelete['qty']

    tablesCollection.update_one({"_id": ObjectId(productDelete['tableId'])}, {"$set": table})
    print(productDelete)

    findUser = userCollection.find_one({"_id": ObjectId(productDelete["userId"])})

    employersCollection.update_one({"email": findUser["email"]}, {"$inc": {"income": product_price}})

    productsCollection.delete_one({"_id": ObjectId(id)})

