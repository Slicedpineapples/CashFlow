import os
from welcome import login, signUp
from income import income
from expenses import expenses
from assets import assets
from liabilities import liabilities
from reports import incomeReport, expensesReport, assetsReport, liabilitiesReport


import os

def mainApp():
    global userId
    global userName

    print("Welcome to MoneyMaster")
    print("1. Sign up")
    print("2. Login")
    print("Q. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        userId = signUp()
    elif choice == "2":
        userId = login()
        # print(userId) Debugging only
    elif (choice == "q" or choice == "Q"):
        print("Exiting...")
        os.system("clear")  # For Linux/OS X
        exit()
    else:
        print("Invalid choice. Try again.")
        mainApp()

    # create_reports_directory()  # Ensure 'reports' directory exists

    while userId is not None:
        print("1. Add income")
        print("2. Add expense")
        print("3. Add asset")
        print("4. Add liability")
        print("5. Generate reports")
        print("q. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            income(userId, 1, 1)
        elif choice == "2":
            expenses(1, 1, userId)
        elif choice == "3":
            assets(1, userId)
        elif choice == "4":
            liabilities(1, userId)
        elif choice == "5":
            print("Reports Available")
            print("1. Income report")
            print("2. Expenses report")
            print("3. Assets report")
            print("4. Liabilities report")
            print("5. Net worth report")
            print("q. Quit")
            choice = input("Choose report to generate: ")
            if choice == "1":
                incomeReport(userId)
            elif choice == "2":
                expensesReport(userId)
            elif choice == "3":
                assetsReport(userId)
            elif choice == "4":
                liabilitiesReport(userId)
            elif choice == "5":
                print("Net worth report")
            elif choice == "q":
                print("Logging out...")
                # mainApp()
                break
            else:
                print("Invalid choice. Try again.")
                continue
        elif choice == "q":
            print("Logging out...")
            # mainApp()
            break
        else:
            print("Invalid choice. Try again.")
            continue

try:
    mainApp()
except Exception as e:
    print("Something went wrong:", e)
    mainApp()