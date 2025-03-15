from server import connect
import datetime
import requests
from utils import ustVerify

def incomeSource(sourceName, amount):
    # sourceName = conninput("Enter the name of the income source: ") 
    # amount = input("Enter the amount of income: ")
    sourceName = sourceName
    amount = amount

    incomeSrc = connect()
    cursor = incomeSrc.cursor()

    sql = "INSERT INTO incomeSource (sourceName, amount) VALUES (%s, %s)"
    values = (sourceName, amount)
    cursor.execute(sql, values)
    incomeSrc.commit()

    print("Income source added successfully!")
    cursor.execute("SELECT LAST_INSERT_ID()")
    sourceId = cursor.fetchone()[0]
    cursor.close()
    if sourceId:
        return sourceId
    else:
        return None



def incomeCategory(categoryName):
    # incomeName = input("Enter the category of the income: ")
    incomeName = categoryName

    incomeCat = connect()
    cursor = incomeCat.cursor()

    sql = "INSERT INTO incomeCategory (incomeName) VALUES (%s)"
    values = (incomeName,)
    cursor.execute(sql, values)
    incomeCat.commit()
    print("Income category added successfully!")

    cursor.execute("SELECT LAST_INSERT_ID()")
    icId = cursor.fetchone()[0]
    cursor.close()
    if icId:
        return icId
    else:
        return None
       

def currency():#Not yet complete
    currencyName = input("Enter the currency name: ")
    currency = connect()

    def get_exchange_rate(base_currency, target_currency):
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url)
        data = response.json()
        exchange_rate = data['rates'][target_currency]
        return exchange_rate

    usd_to_huf = get_exchange_rate("USD", "HUF")
    ksh_to_huf = get_exchange_rate("KSH", "HUF")
    cursor = currency.cursor()

    sql = "INSERT INTO currency (currencyName, currencySymbol) VALUES (%s, %s)"
    values = (currencyName, currencySymbol)
    cursor.execute(sql, values)
    currency.commit()
    print("Currency added successfully!")



    cursor.close()

def income(userId, sourceAmountId, IncomeCategoryId, ust):
    # userId = login()
    # sourceAmountId = incomeSource()
    # IncomeCategoryId = incomeCategory()
    userId = userId
    sourceAmountId = sourceAmountId
    IncomeCategoryId = IncomeCategoryId
    currencyId = 1 # for now
    date= datetime.datetime.now()
    if ustVerify(ust) == False:
        return "Invalid User Security Token"
    else:
        connection = connect()
        cursor = connection.cursor()
        sql = "INSERT INTO income (sourceAmountId, IncomeCategoryId, currId, date, userId) VALUES (%s, %s, %s, %s, %s)"
        values = (sourceAmountId, IncomeCategoryId, currencyId, date, userId)
        cursor.execute(sql, values)
        connection.commit()
        print("Income added successfully!")
        cursor.close()
        if cursor.rowcount > 0:
            return "success"
        else:
            return "failed"

# income(20, 1, 1, "52cd1346eb6725617c5e951418e987cab94b165ac094f3de4c450d679d083243") # Debugging only