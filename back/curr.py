import requests

def get_currency(country_name: str):
    """Fetches the currency code for a given country using the REST API."""
    
    if not country_name or not isinstance(country_name, str):
        return "Error: Invalid country name provided."

    url = f"https://restcountries.com/v3.1/name/{country_name.strip().capitalize()}"

    try:
        response = requests.get(url, timeout=5)  # Set timeout to prevent long waits
        response.raise_for_status()  # Raise an error for HTTP errors (4xx, 5xx)

        data = response.json()

        if not data or not isinstance(data, list):  # Ensure response is a list
            return f"Error: No matching country found for '{country_name}'."

        country_info = data[0]  # Get the first match
        currencies = country_info.get("currencies", {})

        if not currencies:  # If no currencies are found
            return f"Error: Currency information unavailable for '{country_name}'."

        currency_code = list(currencies.keys())[0]  # Extract first currency code
        return currency_code

    except requests.exceptions.Timeout:
        return "Error: Request timed out. Please check your internet connection."
    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect. Check your internet connection."
    except requests.exceptions.HTTPError as http_err:
        return f"Error: HTTP error occurred - {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Error: Failed to retrieve currency - {req_err}"
    except (IndexError, KeyError, TypeError):
        return f"Error: Unexpected data format received for '{country_name}'."

# Debugging only
# print(get_currency("keNYA"))  # Expected output: "KES"
# print(get_currency("Hungary"))  # Expected output: "HUF"
# print(get_currency("InvalidCountry"))  # Expected error message
