from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def apis(change='USD'):

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start': 1,
    'limit': 2,
    'convert': change
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '94cc259d-0784-4fb2-bd01-4b0f9dc3926f',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


# ARF = 'ARS'
# apis(ARF)
apis()


