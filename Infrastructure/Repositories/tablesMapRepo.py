from bson import ObjectId
from Utils.Exceptions.customExceptions import CustomException
from Domain.extensions import tablesMapCollection,userCollection,productsHistoryCollection


def createTableMapRepo(adminId):

    # Ensure that the user exists in MongoDB
    user = userCollection.find_one({"_id": ObjectId(adminId)})

    if user is None:

        raise CustomException(404, "The user does not exist")

    if user["role"] == "admin":

        newTableMap = {
            "adminId": adminId,
            "totalRows": 0,
            "totalColumns": 0,
            "cells": 0,
        }

        tablesMapCollection.insert_one(newTableMap)

    else:

        raise CustomException(403, "You are not allowed to create a table map")

def updateTableMapRepo(adminId,newTableMap):

    user = userCollection.find_one({"_id": ObjectId(adminId)})

    if user is None:
        raise CustomException(404, "The user does not exist")

    if user["role"] == "admin":

        tableMap = tablesMapCollection.find_one({"adminId": adminId})

        if tableMap is None:

            raise CustomException(404, "Table map does not exist")

        else:

            tablesMapCollection.update_one(
                {"adminId": adminId},
                {"$set": {
                    "cells": newTableMap["cells"],
                    "totalRows": newTableMap["totalRows"],
                    "totalColumns": newTableMap["totalColumns"]
                }}
            )

            return {"message": "Table map updated"}

    else:

        raise CustomException(403, "You are not allowed to update a table map")

def getTableMapRepo(adminId):

    user = userCollection.find_one({"_id": ObjectId(adminId)})

    if user is None:

        raise CustomException(404, "The user does not exist")


    tableMap = tablesMapCollection.find_one({"adminId": adminId})

    if tableMap is None:

        raise CustomException(404, "Table map does not exist")

    tableMap["_id"] = str(tableMap["_id"])

    return tableMap



