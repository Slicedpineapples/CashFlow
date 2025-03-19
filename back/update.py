from curr import get_currency
from server import connect
from utils import ustVerify

def updateCountry(userid, newCountry, ust):
    if ustVerify(userid, ust) == False:
        return "Invalid session"
    else:
        try:
            # Validate input
            if not userid or not newCountry:
                return "Error: User ID and country are required."

            # Capitalize country name
            region = newCountry.strip().capitalize()
            newcurr = get_currency(region)

            if not newcurr:
                return f"Error: Could not determine currency for {region}."

            # Establish DB connection
            updateconn = connect()
            cursor = updateconn.cursor()

            # Update user region and currency
            sql = '''UPDATE user SET region = %s, currency = %s WHERE id = %s'''
            values = (region, newcurr, userid)
            cursor.execute(sql, values)
            updateconn.commit()
            message = "Country updated successfully!"

            return newcurr, newCountry, message

        except Exception as e:
            print(f"Database error: {e}")
            return f"Error updating country: {e}"

        finally:
            # Ensure cursor and connection are properly closed
            if cursor:
                cursor.close()
            if updateconn:
                updateconn.close()

# Debugging only
# print(updateCountry(1, "kenya"))  # Expected output: "KES, Kenya, Country updated successfully!"