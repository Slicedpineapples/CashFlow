from server import connect
import datetime
from utils import ustVerify
def assetsCategory(name, numberOfItems, location):
    # name = input("Enter the name of the asset category: ")
    # numberOfItems = input("Enter the number of items: ")
    # location = input("Enter the location of the asset: ")
    name = name
    numberOfItems = numberOfItems
    location = location

    assetsCategory = connect()
    cursor = assetsCategory.cursor()
    sql = "INSERT INTO assetsCategory (AssetName, numberOfItems, location) VALUES (%s, %s, %s)"
    values = (name, numberOfItems, location)
    cursor.execute(sql, values)
    assetsCategory.commit()
    print("Asset category added successfully!")

    cursor.execute("SELECT LAST_INSERT_ID()")
    assetCategoryId = cursor.fetchone()[0]
    cursor.close()
    assetsCategory.close()
    if assetCategoryId:
        return assetCategoryId
    else:
        return None

def assets(assetCategoryId, userId, value, ust):
    if ustVerify(ust) == False:
        return "Invalid session"
    else:
        assetCategoryId = assetCategoryId
        userId = userId
        
        
        # value = input("Enter the value of the asset: ")
        # print('Enter the date of purchase:')
        # date = Date()
        value = value
        date = datetime.datetime.now()


        assets = connect()
        cursor = assets.cursor()
        sql = "INSERT INTO assets (assetCategoryId, value, date, userId) VALUES (%s, %s, %s, %s)"
        values = (assetCategoryId, value, date, userId)
        cursor.execute(sql, values)
        assets.commit()
        print("Asset added successfully!")
        cursor.close()
        assets.close()
        if assetCategoryId:
            return "success"
        else:
            return "failed"
        
# print(assets(1, 20, 1000, "03797f39fce6c045a86a74b96ae86e850435fdea4988e37c272e3ff539e5b776")) # Debugging only

