import requests

user = 'yoonjaejasonlee'
token = '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'

url =  "https://api.github.com/rate_limit"
response = requests.get(url, auth=(user, token))

responses = response.json()

print(responses)