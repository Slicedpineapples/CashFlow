from server import connect
import datetime

def liabilitiescategory(name, grossAmount, remainingAmount):
    # print("Liabilities")
    # print("1. Mortgage")
    # print("2. Student Loan")
    # print("3. Car Loan")
    # print("4. Credit Card")
    # print("5. Personal Loan")
    # print("6. Other")
    # print("7. Exit")
    # choice = input("Enter your choice: ")
    # return choice
    # name = input("Enter the name of the liability category: ")
    # grossAmount = input("Enter the gross amount: ")
    # remainingAmount = input("Enter the remaining amount: ")
    name = name
    grossAmount = grossAmount
    remainingAmount = remainingAmount

    liabilitiesCategory = connect()
    cursor = liabilitiesCategory.cursor()
    sql = "INSERT INTO liabilitiesCategory (liabilityName, grossAmount, remainingAmount) VALUES (%s, %s, %s)"
    values = (name, grossAmount, remainingAmount)
    cursor.execute(sql, values)
    liabilitiesCategory.commit()
    print("Liability category added successfully!")

    cursor.execute("SELECT LAST_INSERT_ID()")
    liabilityCategoryId = cursor.fetchone()[0]
    return liabilityCategoryId

def liabilities(liabilityCategoryId, userId):
    
    # liabilityCategoryId = liabilitiescategory()
    liabilityCategoryId = liabilityCategoryId
    userId = userId
    date = datetime.datetime.now()
    
    liabilities = connect()
    cursor = liabilities.cursor()
    sql = "INSERT INTO liabilities (liabilityCategoryId, dateDue, userId) VALUES (%s, %s, %s)"
    values = (liabilityCategoryId, date, userId)
    cursor.execute(sql, values)
    liabilities.commit()
    print("Liability added successfully!")
    cursor.close()
    liabilities.close()
    if liabilityCategoryId:
        return "success"
    else:
        return "failed"