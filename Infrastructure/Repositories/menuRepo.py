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
        "description": productData["description"],
        "deleted": False
    }
    
    productId = menuCollection.insert_one(newProduct).inserted_id
    newProduct["_id"] = str(productId)

    return newProduct


def getProductsFromMenuRepo(adminId, page):

    limit = 10
    skip = (page - 1) * limit

    admin = userCollection.find_one({"_id": ObjectId(adminId)})

    if admin is None:
        raise CustomException(404, "Admin not found")

    products = menuCollection.find({"adminId": adminId, "deleted": False}).skip(skip).limit(limit)

    return list(products)
def deleteProductFromMenuRepo(prodId):

    product = menuCollection.find_one({"_id": ObjectId(prodId)})
    if product is None:
        raise CustomException(404, "Product not found")

    imageUrlData = product["imageUrl"].split('/')[-1]

    if imageUrlData != "noimage.jpg":
        deleteImageFromBlob(product["imageUrl"], "foodimages")
        menuCollection.update_one({"_id": ObjectId(prodId)}, {"$set": {"deleted": True}})

    else:

        menuCollection.update_one({"_id": ObjectId(prodId)}, {"$set": {"deleted": True}})



def updateProductMenuRepo(newProductData,productId):

    product = menuCollection.find_one({"_id": ObjectId(productId)})
    if product is None:
        raise CustomException(404, "Product not found")

    menuCollection.update_one({"_id": ObjectId(productId)}, {"$set": newProductData})


def searchProductInMenuRepo(adminId, productName):
    query = {"adminId": adminId, "deleted": False}
    query["name"] = {"$regex": productName, "$options": "i"}  # Match anywhere, case-insensitive

    products = menuCollection.find(query).limit(5)
    products_list = list(products)

    if not products_list:
        raise CustomException(404, "Product not found")

    menuProducts = []

    for product in products_list:
        newProduct = {
            "_id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
            "type": product["type"],
            "imageUrl": product["imageUrl"],
            "description": product["description"]
        }
        menuProducts.append(newProduct)

    return menuProducts


