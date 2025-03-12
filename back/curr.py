import requests

def get_currency(country_name: str):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"Could not determine the country for: {country_name}"
    
    data = response.json()
    if not data:
        return f"Could not find a matching country for: {country_name}"
    
    country_info = data[0]  # Get the first match
    currencies = country_info.get("currencies", {})
    
    if not currencies:
        return f"Could not find currency information for: {country_name}"
    
    currency_code = list(currencies.keys())[0]
    return currency_code

# Debuggig only
# print(get_currency("keNYA"))
# print(get_currency("hungary"))

#To update the base currency when the user changes their account
