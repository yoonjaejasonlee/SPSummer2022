import requests
from prettytable import PrettyTable


table2 = PrettyTable()
table2.field_names = ["URL"]

user = 'yoonjaejasonlee'
token = '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'

authorization = f'token {token}'
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization" : authorization,
    }

name = "github"


api_url = f"https://api.github.com/search/code?q=user:{name}+extension:py&per_page=100"

#send get request
response = requests.get(api_url,auth=(user,token))

#get the json data
data =  response.json()

for repository in data["items"]:
    name = repository["html_url"]
    
    table2.add_row([name])

    
print(table2)

rl = requests.get("https://api.github.com/rate_limit", auth=(user,token))

data2 = rl.json()

print(data2)
print(data["total_count"])



    