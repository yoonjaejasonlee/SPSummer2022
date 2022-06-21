from flask import jsonify
import requests
from prettytable import PrettyTable

table = PrettyTable()
table.field_names = ["User Name", "Created Date", "Language", "Stars", "Forks", "URL"]

user = 'yoonjaejasonlee'
token = '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'

authorization = f'token {token}'
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": authorization,
}


i = 1

langs = "python"
stars = 3000
forks = 200

api_url = "https://api.github.com/search/repositories?q=language:python+stars:%3E=100000+forks:%3E=30&page=1&per_page=10"

# send get request
response = requests.get(api_url, auth=(user, token))

# get the json data
data = response.json()

for repository in data["items"]:
    names = repository["name"]
    created_date = repository["created_at"]
    language = repository["language"]
    stars = repository["stargazers_count"]
    forks = repository["forks"]
    url = repository["html_url"]

    table.add_row([names, created_date, language, stars, forks, url])

print(table)
