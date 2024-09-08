from Domain.extensions import productsHistoryCollection
from datetime import datetime, timedelta

def dailyEmployeeSalesForCurrentMonth(userId):
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
                    "userId": userId,  # Filter by userId instead of adminId
                    "timeStamp": {"$gte": day_start, "$lte": day_end}
                }
            },
            {
                "$group": {
                    "_id": "$menuProductId",  # Group by menu product ID
                    "qtySum": {"$sum": "$qty"}  # Sum quantities sold for each product
                }
            },
            {
                "$lookup": {
                    "from": "menu",
                    'let': {"searchId": {"$toString": "$_id"}},  # Convert _id to string
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$eq": ["$_id", {"$toObjectId": "$$searchId"}]  # Match with the product in the menu
                                }
                            }
                        },
                        {
                            "$project": {
                                "_id": 0,
                                "price": 1  # Retrieve only the price field
                            }
                        }
                    ],
                    "as": "productDetails"
                }
            },
            {
                "$unwind": "$productDetails"  # Flatten the productDetails array
            },
            {
                "$project": {
                    "_id": 0,
                    "qtySum": 1,
                    "price": "$productDetails.price"  # Include only the price from the menu
                }
            }
        ]

        # Execute the pipeline
        day_sales = list(productsHistoryCollection.aggregate(pipeline))

        # Initialize daily total sales
        totalSum = 0

        # Process each product in day_sales
        for product in day_sales:
            qty = product["qtySum"]
            price = product.get("price", 0)  # Get the price, default to 0 if not available
            totalSum += qty * price

        # Append the result for the day
        result.append({"day": day, "totalSum": totalSum})

    return result


def monthlyEmployeeSalesForCurrentYear(userId):
    # Get the current date and year
    currentYear = datetime.now().year

    # Initialize the list to hold the monthly sales data
    result = []

    # Loop through each month from January (1) to the current month
    for month in range(1, datetime.now().month + 1):
        # Calculate the start and end timestamps for the current month
        month_start = datetime(currentYear, month, 1, 0, 0, 0)

        # If it's the current month, set the end date to today, otherwise use the last day of the month
        if month == datetime.now().month:
            month_end = datetime.now()
        else:
            # Calculate the last day of the month
            next_month = month + 1 if month < 12 else 1
            next_month_year = currentYear if month < 12 else currentYear + 1
            month_end = datetime(next_month_year, next_month, 1, 0, 0, 0) - timedelta(seconds=1)

        pipeline = [
            {
                "$match": {
                    "userId": userId,  # Filter by userId
                    "timeStamp": {"$gte": month_start, "$lte": month_end}  # Filter by month range
                }
            },
            {
                "$group": {
                    "_id": "$menuProductId",  # Group by menu product ID
                    "qtySum": {"$sum": "$qty"}  # Sum quantities sold for each product
                }
            },
            {
                "$lookup": {
                    "from": "menu",
                    'let': {"searchId": {"$toString": "$_id"}},  # Convert _id to string
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$eq": ["$_id", {"$toObjectId": "$$searchId"}]  # Match with the product in the menu
                                }
                            }
                        },
                        {
                            "$project": {
                                "_id": 0,
                                "price": 1  # Retrieve only the price field
                            }
                        }
                    ],
                    "as": "productDetails"
                }
            },
            {
                "$unwind": "$productDetails"  # Flatten the productDetails array
            },
            {
                "$project": {
                    "_id": 0,
                    "qtySum": 1,
                    "price": "$productDetails.price"  # Include only the price from the menu
                }
            }
        ]

        # Execute the pipeline
        month_sales = list(productsHistoryCollection.aggregate(pipeline))

        # Initialize monthly total sales
        totalSum = 0

        # Process each product in month_sales
        for product in month_sales:
            qty = product["qtySum"]
            price = product.get("price", 0)  # Get the price, default to 0 if not available
            totalSum += qty * price

        # Append the result for the month
        result.append({"month": month, "totalSum": totalSum})

    return result
