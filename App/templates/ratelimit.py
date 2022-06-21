import requests

user = 'yoonjaejasonlee'
token = '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'

url = "https://api.github.com/rate_limit"

rate_limit = requests.get(url, auth=(user, token))

response = rate_limit.json()


print(response)

