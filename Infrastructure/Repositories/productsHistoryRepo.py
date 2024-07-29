from datetime import datetime
from Domain.extensions import productsHistoryCollection


def getSoldProducts(adminId, startDate, endDate):

    try:

        start_timestamp = datetime.fromisoformat(startDate)
        end_timestamp = datetime.fromisoformat(endDate)

    except ValueError:
        raise ValueError("Invalid date format. Use ISO 8601 format (e.g., '2024-06-04T14:05:34.854+00:00')")

    query = {
        "adminId": adminId,
        "timeStamp": {"$gte": start_timestamp, "$lte": end_timestamp}
    }

    products = list(productsHistoryCollection.find(query))

    for product in products:

        product["_id"] = str(product["_id"])
        product["timeStamp"] = product["timeStamp"].isoformat()

    return products
