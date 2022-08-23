from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url_test = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
url_prod = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'e6fc58a7-08be-4996-84ee-72fea95a081e',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url_prod, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)