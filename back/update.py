from curr import get_currency
from server import connect

def updateCountry(userid, newCountry):
    userid = userid
    region = newCountry.capitalize()
    newcurr = get_currency(region)

    updateconn =  connect()
    cursor = updateconn.cursor()

    sql = '''UPDATE user SET region = %s, currency = %s WHERE id = %s'''
    values = (region, newcurr, userid)
    cursor.execute(sql, values)

    updateconn.commit()
    updateconn.close()
    return "Country updated successfully!"

# Debugging only
# print(updateCountry(1, "botswana"))