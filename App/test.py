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


api_url = f"https://api.github.com/search/repositories?q=language:python+stars:%3E=30+forks:%3E=30&page=1&per_page=1"

response = requests.get(api_url)

data = response.json()
urls = data["total_count"]
names = data["incomplete_results"]

print(urls)
print(names)