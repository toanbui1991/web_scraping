import requests
from requests.auth import HTTPBasicAuth
from config import config

#settings
target_link = 'https://finance.vietstock.vn/doanh-nghiep-a-z/?page=1'
user = config.get('user')
password = config.get('password')
auth = HTTPBasicAuth(user, password)
response = requests.get(target_link, auth=auth)

# json = response.json()
# print('json: ')
# print(json)
text = response.text
print('text: ')
print(text)