import datetime
from server import connect

def expensesPrice(itemName, price):
    # print("This is the expense price function")
    # itemName = input("Enter the name of the item: ")
    # price = input("Enter the price of the item: ")
    itemName = itemName
    price = price

    expensesPrice = connect()
    cursor = expensesPrice.cursor()
    sql = "INSERT INTO expensesPrice (itemName, price) VALUES (%s, %s)"

    values = (itemName, price)
    cursor.execute(sql, values)
    expensesPrice.commit()
    print("Expense price added successfully!")

    cursor.execute("SELECT LAST_INSERT_ID()")
    itemId = cursor.fetchone()[0]
    if itemId:
        return itemId
    else:
        return None

def expensesCategory(categoryName):
    # print("This is the expense category function")
    # categoryName = input("Enter the name of the category: ")
    categoryName = categoryName

    expensesCategory = connect()
    cursor = expensesCategory.cursor()
    sql = "INSERT INTO expensesCategory (expenseName) VALUES (%s)"

    values = (categoryName,)
    cursor.execute(sql, values)
    expensesCategory.commit()
    print("Expense category added successfully!")

    cursor.execute("SELECT LAST_INSERT_ID()")
    categoryId = cursor.fetchone()[0]
    if categoryId:
        return categoryId
    else:
        return None

def expenses(expensesPriceId, expenseCategoryId, userId):
    # expensesPriceId = expensesPrice()
    # expenseCategoryId = expensesCategory()
    currId = 1 # for now
    # userId = login()
    date = datetime.datetime.now()
    expensesPriceId = expensesPriceId
    expenseCategoryId = expenseCategoryId
    userId = userId
    print("Enter the date of the transaction:")
    # date = Date()
    
    expenses = connect()
    cursor = expenses.cursor()

    sql = "INSERT INTO expenses (expensesPriceId, currId, expenseCategoryId, userId, date) VALUES (%s, %s, %s, %s, %s)"
    values = (expenseCategoryId, currId, expensesPriceId, userId, date)
    cursor.execute(sql, values)
    expenses.commit()

    print("Expense added successfully!")
    cursor.close()
    expenses.close()
    if cursor.lastrowid:
        return "success"
    else:
        return "failure"



