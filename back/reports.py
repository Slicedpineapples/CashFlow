from server import connect
from utils import Date, makeDir
import datetime

makeDir() 

def incomeReport(userId, start, end):
    income = connect()
    cursor = income.cursor()

    cursor.execute("SELECT sourceAmountId, incomeCategoryId, date FROM income WHERE userId = %s AND date BETWEEN %s AND %s", (userId, start, end))
    result1 = cursor.fetchall()

    report_path = f'reports/IncomeReports/IR-UID-{userId}-{start}-to-{end}.txt'
    with open(report_path, "w") as report_file:
        report_file.write(f'Income report starting {start} to {end}\n')
        report_file.write("Source\tAmount\tCategory\tDate\n")

        report_data = []
        for row in result1:
            sourceAmountId = row[0]
            incomeCategoryId = row[1]
            date = row[2]

            cursor.execute("SELECT sourceName, amount FROM incomeSource WHERE id = %s", (sourceAmountId,))
            result2 = cursor.fetchall()
            sourceName = result2[0][0]
            amount = result2[0][1]

            cursor.execute("SELECT incomeName FROM incomeCategory WHERE id = %s", (incomeCategoryId,))
            result3 = cursor.fetchall()
            incomeName = result3[0][0]

            report_file.write(f"{sourceName}\t{amount}\t{incomeName}\t{date}\n")

            report_data.append({
                "sourceName": sourceName,
                "amount": amount,
                "incomeName": incomeName,
                "date": date
            })
        total_income = sum([data['amount'] for data in report_data])
        total_income = ({"Total" : total_income})
        report_file.write(f"\nTotal Income: {total_income}")
        report_file.write(f'\nReport generated for user {userId} on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    return report_path, report_data, total_income

def expensesReport(userId, start, end):
    start = start
    end = end
    userId = userId
    expenses = connect()
    cursor = expenses.cursor()

    cursor.execute("SELECT expenseCategoryId, expensesPriceId, date FROM expenses WHERE userId = %s AND date BETWEEN %s AND %s", (userId, start, end))
    result1 = cursor.fetchall()

    report_path = f'reports/ExpensesReports/ER-UID-{userId}-{start}-to-{end}.txt'
    with open(report_path, "w") as report_file:
        report_file.write(f'Expenses report starting {start} to {end}\n')
        report_file.write("Category\tItem name\tPrice\tDate\n")

        report_data = []
        for row in result1:
            expenseCategoryId = row[0]
            expensesPriceId = row[1]
            date = row[2]

            cursor.execute("SELECT expenseName FROM expensesCategory WHERE id = %s", (expenseCategoryId,))
            result2 = cursor.fetchall()
            expenseName = result2[0][0]

            cursor.execute("SELECT itemName, Price FROM expensesPrice WHERE id = %s", (expensesPriceId,))
            result3 = cursor.fetchall()
            itemName = result3[0][0]
            price = result3[0][1]

            report_file.write(f"{expenseName}\t{itemName}\t{price}\t{date}\n")

            report_data.append({
                "expenseName": expenseName,
                "itemName": itemName,
                "price": price,
                "date": date,
            })
        total_expenses = sum([data['price'] for data in report_data])
        total_expenses = ({"Total" : total_expenses})
        report_file.write(f"\nTotal Expenses: {total_expenses}")
        report_file.write(f'\nReport generated for user {userId} on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    cursor.close()
    return report_path, report_data, total_expenses

def assetsReport(userId, start, end):
    userId = userId
    start = start
    end = end

    assets = connect()
    cursor = assets.cursor()

    cursor.execute("SELECT assetCategoryId, value, date FROM assets WHERE userId = %s AND date BETWEEN %s AND %s", (userId, start, end))
    result1 = cursor.fetchall()

    report_path = f'reports/AssetsReports/AR-UID-{userId}-{start}-to-{end}.txt'
    with open(report_path, "w") as report_file:
        report_file.write(f'Assets report starting {start} to {end}\n')
        report_file.write("Location\tAsset Name\tValue\tNumber of Items\tDate\n")

        report_data = []
        for row in result1:
            assetCategoryId = row[0]
            value = row[1]
            date = row[2]

            cursor.execute("SELECT assetName, numberOfItems, location FROM assetsCategory WHERE id = %s", (assetCategoryId,))
            result2 = cursor.fetchall()
            assetName = result2[0][0]
            numberOfItems = result2[0][1]
            location = result2[0][2]

            report_file.write(f"{location}\t{assetName}\t{value}\t{numberOfItems}\t{date}\n")

            report_data.append({
                "location": location,
                "assetName": assetName,
                "value": value,
                "numberOfItems": numberOfItems,
                "date": date
            })
        total_assets = sum([data['value'] for data in report_data])
        total_assets = ({"Total" : total_assets})
        report_file.write(f"\nTotal Assets: {total_assets}")
        report_file.write(f'\nReport generated for user {userId} on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    cursor.close()
    return report_path, report_data, total_assets

def liabilitiesReport(userId, start, end):
    userId = userId
    start = start
    end = end

    liabilities = connect()
    cursor = liabilities.cursor()

    cursor.execute("SELECT liabilityCategoryId, dateDue FROM liabilities WHERE userId = %s AND dateDue BETWEEN %s AND %s", (userId, start, end))
    result1 = cursor.fetchall()

    report_path = f'reports/LiabilitiesReports/LR-UID-{userId}-{start}-to-{end}.txt'
    with open(report_path, "w") as report_file:
        report_file.write(f'Liabilities report starting {start} to {end}\n')
        report_file.write("Liability\tGross Amount\tRemaining Amount\tDate Due\n")

        report_data = []
        for row in result1:
            liabilityCategoryId = row[0]
            dateDue = row[1]

            cursor.execute("SELECT liabilityName, grossAmount, remainingAmount FROM liabilitiesCategory WHERE id = %s", (liabilityCategoryId,))
            result2 = cursor.fetchall()
            liabilityName = result2[0][0]
            grossAmount = result2[0][1]
            remainingAmount = result2[0][2]

            report_file.write(f"{liabilityName}\t{grossAmount}\t{remainingAmount}\t{dateDue}\n")

            report_data.append({
                "liabilityName": liabilityName,
                "grossAmount": grossAmount,
                "remainingAmount": remainingAmount,
                "dateDue": dateDue
            })
        total_remaining = sum([data['remainingAmount'] for data in report_data])
        total_Gross = sum([data['grossAmount'] for data in report_data])
        total_liabilities = total_Gross - total_remaining
        total_liabilities = ({"Total" : total_liabilities})
        report_file.write(f"\nTotal Liabilities: {total_liabilities}")# To work on the logic
        report_file.write(f'\nReport generated for user {userId} on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    cursor.close()
    return report_path, report_data, total_liabilities


# incomeReport(1, Date(), Date())
# expensesReport(1)
# assetsReport(1)
# liabilitiesReport(1)