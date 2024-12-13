from datetime import datetime, timedelta
from Domain.extensions import productsHistoryCollection
from bson import ObjectId
import json



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

def getGeneralChartRepo(adminId, startDate, endDate):
    try:
        startTimestamp = datetime.fromisoformat(startDate)
        endTimestamp = datetime.fromisoformat(endDate)
    except ValueError:
        raise ValueError("Invalid date format. Use ISO 8601 format (e.g., '2024-06-04T14:05:34.854+00:00')")

    # The pipeline must be a list of stages
    # The pipeline must be a list of stages
    pipeline = [
        {
            "$match": {
                "adminId": adminId,
                "timeStamp": {"$gte": startTimestamp, "$lte": endTimestamp}
            }
        },
        {
            "$group": {
                "_id": "$menuProductId",
                "qtySum": {"$sum": "$qty"}
            }
        },
        {
            "$sort": {
                "qtySum": -1
            }
        },
        {
            "$lookup": {
                "from": "menu",
                'let': {"searchId": {"$toString": "$_id"}},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$eq": ["$_id", {"$toObjectId": "$$searchId"}]
                            }
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,

                        }
                    }
                ],
                "as": "productDetails"
            }
        }
    ]

    queryResult = list(productsHistoryCollection.aggregate(pipeline))
    print(queryResult[1]["productDetails"][0]["name"])


    return queryResult


def currentDayChartRepo(adminId):

    startTimestamp = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    endTimestamp = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

    pipeline = [
        {
            "$match": {
                "adminId": adminId,
                "timeStamp": {"$gte": startTimestamp, "$lte": endTimestamp}
            }
        },
        {
            "$group": {
                "_id": "$menuProductId",
                "qtySum": {"$sum": "$qty"}
            }
        },
        {
            "$sort": {
                "qtySum": -1  # Sort by qtySum in descending order
            }
        },
        {
            "$lookup": {
                "from": "menu",
                'let': {"searchId": {"$toString": "$_id"}},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$eq": ["$_id", {"$toObjectId": "$$searchId"}]
                            }
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "adminId":0,
                        }
                    }
                ],
                "as": "productDetails"
            }
        }
    ]

    queryResult = list(productsHistoryCollection.aggregate(pipeline))

    return queryResult


def currentMonthChartRepo(adminId):
    # Get the start of the current month
    startTimestamp = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Get the end of the current month
    next_month = startTimestamp.replace(month=startTimestamp.month % 12 + 1, day=1, hour=0, minute=0, second=0,
                                        microsecond=0)
    endTimestamp = next_month - timedelta(microseconds=1)
    print(adminId)
    pipeline = [
        {
            "$match": {
                "adminId": adminId,
            }
        },
        {
            "$group": {
                "_id": "$menuProductId",
                "qtySum": {"$sum": "$qty"}
            }
        },
        {
            "$sort": {
                "qtySum": -1  # Sort by qtySum in descending order
            }
        },
        {
            "$lookup": {
                "from": "menu",
                'let': {"searchId": {"$toString": "$_id"}},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$eq": ["$_id", {"$toObjectId": "$$searchId"}]
                            }
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "adminId": 0,
                        }
                    }
                ],
                "as": "productDetails"
            }
        }

    ]

    queryResult = list(productsHistoryCollection.aggregate(pipeline))

    result = []

    for product in queryResult:
        product["_id"] = str(product["_id"])

        result.append(product)

    return result


def dailySalesForCurrentMonth(adminId):
    # Get the start of the current month
    startTimestamp = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Get today's date
    today = datetime.now()

    # Initialize the list to hold the daily sales data
    result = []

    # Loop through each day of the current month up to today
    for day in range(1, today.day + 1):
        # Calculate the start and end time for the current day
        day_start = startTimestamp.replace(day=day)
        day_end = day_start.replace(hour=23, minute=59, second=59, microsecond=999999)

        pipeline = [
            {
                "$match": {
                    "adminId": adminId,
                    "timeStamp": {"$gte": day_start, "$lte": day_end}
                }
            },
            {
                "$group": {
                    "_id": "$menuProductId",
                    "qtySum": {"$sum": "$qty"}
                }
            },
            {
                "$lookup": {
                    "from": "menu",
                    'let': {"searchId": {"$toString": "$_id"}},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$eq": ["$_id", {"$toObjectId": "$$searchId"}]
                                }
                            }
                        },
                        {
                            "$project": {
                                "_id": 0,
                                "adminId": 0,
                            }
                        }
                    ],
                    "as": "productDetails"
                }
            }
        ]

        # Get the total sales for the current day
        day_sales = list(productsHistoryCollection.aggregate(pipeline))

        # Initialize daily total sales
        totalSum = 0

        # Process each product in day_sales
        for product in day_sales:
            qty = product["qtySum"]
            price = product["productDetails"][0]["price"]
            totalSum += qty * price

        # Append the result for the day
        result.append({"day": day, "totalSum": totalSum})

    # Print the final result list, not during each iteration
    return result


from datetime import datetime
from pymongo import MongoClient

def salesForCurrentYear(adminId):
    # Get the start of the current year
    startOfYear = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    # Get today's date
    today = datetime.now()

    # Initialize the lists to hold the daily and monthly sales data
    dailySales = []
    monthlySales = []

    # Loop through each day of the current month up to today
    startOfMonth = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    for day in range(1, today.day + 1):
        day_start = startOfMonth.replace(day=day)
        day_end = day_start.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Loop through each month of the current year up to the current month
    for month in range(1, today.month + 1):
        month_start = startOfYear.replace(month=month)
        if month == today.month:
            # If it's the current month, end at today's date
            month_end = today.replace(hour=23, minute=59, second=59, microsecond=999999)
        else:
            # Otherwise, end at the last day of the month
            month_end = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(seconds=1)

        pipeline = [
            {
                "$match": {
                    "adminId": adminId,
                    "timeStamp": {"$gte": month_start, "$lte": month_end}
                }
            },
            {
                "$group": {
                    "_id": "$menuProductId",
                    "qtySum": {"$sum": "$qty"}
                }
            },
            {
                "$lookup": {
                    "from": "menu",
                    'let': {"searchId": {"$toString": "$_id"}},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$eq": ["$_id", {"$toObjectId": "$$searchId"}]
                                }
                            }
                        },
                        {
                            "$project": {
                                "_id": 0,
                                "adminId": 0,
                            }
                        }
                    ],
                    "as": "productDetails"
                }
            }
        ]

        month_sales = list(productsHistoryCollection.aggregate(pipeline))
        totalSum = 0

        for product in month_sales:
            qty = product["qtySum"]
            price = product["productDetails"][0]["price"]
            totalSum += qty * price

        monthlySales.append({"month": month, "totalSum": totalSum})

    # Print or return the final results
    print("Monthly Sales for Current Year:", monthlySales)

    return {"monthlySales": monthlySales}
