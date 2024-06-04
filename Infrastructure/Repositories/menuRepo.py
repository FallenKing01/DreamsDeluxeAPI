from bson import ObjectId
from Utils.Exceptions.customExceptions import CustomException
from Domain.extensions import menuCollection, userCollection
from Controllers.uploadController import deleteImageFromBlob

def addProductInMenuRepo(productData,adminId):

    admin = userCollection.find_one({"_id": ObjectId(adminId)})
    if admin is None:
        raise CustomException(404, "Admin not found")
    newProduct = {
        "name": productData["name"].lower(),
        "price": productData["price"],
        "type": productData["type"],
        "adminId": adminId,
        "imageUrl": "https://dreamsblob.blob.core.windows.net/foodimages/noimage.jpg",
        "description": productData["description"]
    }
    productId = menuCollection.insert_one(newProduct).inserted_id
    newProduct["_id"] = str(productId)

    return newProduct

def getProductsFromMenuRepo(adminId):

    admin = userCollection.find_one({"_id": ObjectId(adminId)})

    if admin is None:
        raise CustomException(404, "Admin not found")
    products = menuCollection.find({"adminId": adminId})

    return list(products)

def deleteProductFromMenuRepo(prodId):

    product = menuCollection.find_one({"_id": ObjectId(prodId)})
    if product is None:
        raise CustomException(404, "Product not found")

    imageUrlData = product["imageUrl"].split('/')[-1]

    if imageUrlData != "noimage.jpg":
        deleteImageFromBlob(product["imageUrl"], "foodimages")
        menuCollection.delete_one({"_id": ObjectId(prodId)})


def searchProductFromMenuRepo(productName):
    # Perform a case-insensitive search on the lowercased product names
    products = menuCollection.find({
        "name": {"$regex": f".*{productName}.*", "$options": "i"},
    })

    # Convert MongoDB cursor to a list
    result = list(products)

    if not result:
        raise CustomException(404, f"No products found containing the word: {productName}")

    return result