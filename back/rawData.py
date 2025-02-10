from collections import defaultdict
from server import connect
from collections import defaultdict
from utils import getExchangeRate

#Making a select querry for income. It will fetch all incomes, then categorice them by category and sum them up.The result will be a list of dictionaries.
def incomeRawData(userId, start, end, currency):
    # Connect to the database
    currency = getExchangeRate(currency)
    income = connect()
    cursor = income.cursor()

    # Fetch the relevant income records for the given user and date range
    cursor.execute("SELECT sourceAmountId, incomeCategoryId FROM income WHERE userId = %s AND date BETWEEN %s AND %s", (userId, start, end))
    result1 = cursor.fetchall()

    # Initialize a defaultdict to group income amounts by incomeName
    income_groups = defaultdict(float)  # Use float for better precision during addition

    # Process each income record
    for row in result1:
        sourceAmountId = row[0]
        incomeCategoryId = row[1]

        # Fetch the amount from incomeSource table
        cursor.execute("SELECT amount FROM incomeSource WHERE id = %s", (sourceAmountId,))
        result2 = cursor.fetchone()
        amount = result2[0] * currency if result2 else 0  # Convert the amount to the target currency

        # Fetch the incomeName from incomeCategory table
        cursor.execute("SELECT incomeName FROM incomeCategory WHERE id = %s", (incomeCategoryId,))
        result3 = cursor.fetchone()
        incomeName = result3[0] if result3 else "Unknown"

        # Aggregate the amount by incomeName
        income_groups[incomeName] += amount

    # Prepare the report data
    report_data = []
    for incomeName, total_amount in income_groups.items():
        rounded_total_amount = round(total_amount, 2)
        report_data.append({
            "incomeName": incomeName,
            "amount": rounded_total_amount,
        })

    # Calculate the total income
    total_income = round(sum(round(amount, 2) for amount in income_groups.values()), 2)

    # Close the cursor
    cursor.close()

    # Return the report data and total income
    return report_data, total_income


# print(incomeRawData(2, '2024-05-01', '2024-5-31')[1]) #testing the function

#Making a select querry for expenses. It will fetch all expenses, then categorice them by category and sum them up.The result will be a list of dictionaries.


def expensesRawData(userId, start, end, currency):
    currency = getExchangeRate(currency)
    expenses = connect()
    cursor = expenses.cursor()

    cursor.execute("SELECT expenseCategoryId, expensesPriceId FROM expenses WHERE userId = %s AND date BETWEEN %s AND %s", (userId, start, end))
    result1 = cursor.fetchall()

    expense_groups = defaultdict(float)  # Use float for better precision during addition

    for row in result1:
        expenseCategoryId = row[0]
        expensesPriceId = row[1]

        cursor.execute("SELECT expenseName FROM expensesCategory WHERE id = %s", (expenseCategoryId,))
        result2 = cursor.fetchone()  # Since we are fetching a single value, use fetchone()

        if result2:
            expenseName = result2[0]

            cursor.execute("SELECT Price FROM expensesPrice WHERE id = %s", (expensesPriceId,))
            result3 = cursor.fetchone()

            if result3:
                price = result3[0] * currency  # Convert the price to the target currency
                expense_groups[expenseName] += price

    # Convert grouped dictionary to final report format
    report_data = []
    total_expenses = 0
    for expenseName, total_price in expense_groups.items():
        rounded_total_price = round(total_price, 2)
        report_data.append({
            "expenseName": expenseName,
            "total_price": rounded_total_price,
        })
        total_expenses += rounded_total_price
    cursor.close()

    return report_data, round(total_expenses, 2)


#Making a select querry for assets. It will fetch all assets, then categorice them by category and sum them up.The result will be a list of dictionaries.
def assetsRawData(userId, start, end, currency):
    currency = getExchangeRate(currency)
    assets = connect()
    cursor = assets.cursor()

    cursor.execute("SELECT assetCategoryId, value FROM assets WHERE userId = %s AND date BETWEEN %s AND %s", (userId, start, end))
    result1 = cursor.fetchall()

    report_data = []
    for row in result1:
        assetCategoryId = row[0]
        value = round(row[1]*currency, 2)

        cursor.execute("SELECT assetName, numberOfItems, location FROM assetsCategory WHERE id = %s", (assetCategoryId,))
        result2 = cursor.fetchall()
        assetName = result2[0][0]
        numberOfItems = result2[0][1]
        location = result2[0][2]

        report_data.append({
            "location": location,
            "assetName": assetName,
            "value": value,
            "numberOfItems": numberOfItems,
        })
    total_assets = sum([data['value'] for data in report_data])
    total_assets = ({total_assets})
    total_assets = round(total_assets.pop(), 2)   #parsing it as a float

    cursor.close()
    return report_data, total_assets

#Making a select querry for liabilities. It will fetch all liabilities, then categorice them by category and sum them up.The result will be a list of dictionaries.
def liabilitiesRawData(userId, start, end, currency):
    currency = getExchangeRate(currency)
    liabilities = connect()
    cursor = liabilities.cursor()

    cursor.execute("SELECT liabilityCategoryId, dateDue FROM liabilities WHERE userId = %s AND dateDue BETWEEN %s AND %s", (userId, start, end))
    result1 = cursor.fetchall()

    report_data = []
    for row in result1:
        liabilityCategoryId = row[0]
        dateDue = row[1]

        cursor.execute("SELECT liabilityName, grossAmount, remainingAmount FROM liabilitiesCategory WHERE id = %s", (liabilityCategoryId,))
        result2 = cursor.fetchall()
        liabilityName = result2[0][0]
        grossAmount = round(result2[0][1]*currency, 2)
        remainingAmount = round(result2[0][2]*currency, 2)

        report_data.append({
            "liabilityName": liabilityName,
            "grossAmount": grossAmount,
            "remainingAmount": remainingAmount,
            "dateDue": dateDue
        })
    total_remaining = sum([data['remainingAmount'] for data in report_data])
    total_Gross = sum([data['grossAmount'] for data in report_data])
    total_liabilities = total_Gross - total_remaining
    total_liabilities = ({total_liabilities})
    total_liabilities = round(total_liabilities.pop(), 2)  #parsing it as a float

    cursor.close()
    return report_data, total_liabilities


#Debugging for curreny modiule
# print(incomeRawData(1, '2024-05-01', '2024-5-31', "KES")) #testing the function
# print(expensesRawData(1, '2024-05-01', '2024-6-30', "KES")) #testing the function
# print(assetsRawData(1, '2024-05-01', '2024-5-31', "HUF")) #testing the function
# print(liabilitiesRawData(1, '2024-05-01', '2024-5-31', "HUF")) #testing the function